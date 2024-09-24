import logging
from typing import Annotated
from uuid import UUID, uuid4

from fastapi import APIRouter, Body, Depends, HTTPException, Request, status
from fastapi_users import FastAPIUsers, exceptions, models
from fastapi_users.manager import BaseUserManager
from fastapi_users.router.common import ErrorCode
from fastapi_users.jwt import generate_jwt
from pwdlib.hashers.argon2 import Argon2Hasher

from models.user import User
from security import users
from security.schemas import (
    UserOut,
    CreateUserIn,
    CreateUserDB,
    RegisterUserDB,
    RegisterUserIn,
)
from settings import settings
from utils.send_email import send_email_template


fastapi_users = FastAPIUsers[User, UUID](
    users.fastapi_users.get_user_manager,
    [users.auth_backend],
)

get_current_active_verified_superuser = fastapi_users.authenticator.current_user(
    active=True,
    verified=True,
    superuser=True,
)

logger = logging.getLogger(__name__)

router = APIRouter()


def generate_jwt_reset_password_token(
    user: models.UP,
) -> str:
    """
    Generate a JWT token for resetting the password of a user.

    :param user: The user for which the token should be generated.
    """

    password_hasher = Argon2Hasher()

    token_data = {
        "sub": str(user.id),
        "password_fgpt": password_hasher.hash(user.hashed_password),
        "aud": "fastapi-users:reset",
    }
    reset_password_token_lifetime_seconds: int = 60 * 60 * 24 * 3  # 3 days

    token = generate_jwt(
        token_data,
        settings.auth.reset_password_token_secret,
        reset_password_token_lifetime_seconds,
    )

    return token


@router.post(
    path="/create",
    status_code=status.HTTP_201_CREATED,
    name="create_user",
    dependencies=[Depends(get_current_active_verified_superuser)],
)
async def create_user(
    request: Request,
    create_user: Annotated[
        CreateUserIn, Body(..., description="Informationen des Users")
    ],
    user_manager: Annotated[
        BaseUserManager[models.UP, models.ID], Depends(fastapi_users.get_user_manager)
    ],
):
    # lowercase email
    create_user.email = create_user.email.lower()
    # random placeholder password
    temporary_password = str(uuid4()) + str(uuid4()).upper()
    # create user object
    create_user_db = CreateUserDB(
        **create_user.model_dump(exclude={"is_active", "is_superuser", "is_verified"}),
        is_active=True,
        is_verified=True,
        is_superuser=True,
        password=temporary_password,
    )
    try:
        created_user = await user_manager.create(
            create_user_db, safe=False, request=request
        )
        token = generate_jwt_reset_password_token(created_user)
        reset_domain = (
            f"{settings.email.domain}"
            + f"{settings.email.domain_invite_pwd_suffix}"
            + f"?token={token}"
        )
        await send_email_template(
            email_template="user_invitation_password_email_template.html",
            sender=settings.email.sender,
            recipient=created_user.email,
            subject="Willkommen im CariData Admin-Portal",
            reset_domain=reset_domain,
            domain=settings.email.domain,
        )
    except exceptions.UserAlreadyExists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ein Nutzerkonto mit dieser Email existiert bereits",
        )
    except exceptions.InvalidPasswordException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": ErrorCode.REGISTER_INVALID_PASSWORD,
                "reason": e.reason,
            },
        )


@router.post(
    path="/register",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
    name="register_user",
)
async def register_user(
    request: Request,
    register_user: Annotated[
        RegisterUserIn, Body(..., description="Informationen des Users")
    ],
    user_manager: Annotated[
        BaseUserManager[models.UP, models.ID], Depends(fastapi_users.get_user_manager)
    ],
):
    register_user.email = register_user.email.lower()
    register_user = RegisterUserDB(
        **register_user.model_dump(),
    )
    try:
        created_user = await user_manager.create(
            register_user, safe=True, request=request
        )
        await user_manager.request_verify(created_user, request)
    except exceptions.UserAlreadyExists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ein Nutzerkonto mit dieser Email existiert bereits",
        )
    except exceptions.InvalidPasswordException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": ErrorCode.REGISTER_INVALID_PASSWORD,
                "reason": e.reason,
            },
        )

    return created_user
