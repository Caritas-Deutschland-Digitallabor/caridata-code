import logging
from typing import Annotated, Sequence
from uuid import UUID

from fastapi import (
    APIRouter,
    Body,
    Depends,
    HTTPException,
    Path,
    Request,
    Response,
    status,
)
from fastapi_users import FastAPIUsers, exceptions, models
from fastapi_users.manager import BaseUserManager
from fastapi_users.router.common import ErrorCode
from database.session import get_async_session
from models.user import User
from security import users
from security.schemas import UserOut, UpdateUserDB, UpdateUserIn
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)

router = APIRouter()

fastapi_users = FastAPIUsers[User, UUID](
    users.fastapi_users.get_user_manager,
    [users.auth_backend],
)

get_current_active_user = fastapi_users.authenticator.current_user(
    active=True, verified=False
)

get_current_active_verified_user = fastapi_users.authenticator.current_user(
    active=True, verified=True
)

get_current_active_verified_superuser = fastapi_users.authenticator.current_user(
    active=True, verified=True, superuser=True
)


async def get_user_or_404(
    id: Annotated[UUID, Path(..., description="ID des Users")],
    user_manager: Annotated[
        BaseUserManager[models.UP, models.ID], Depends(fastapi_users.get_user_manager)
    ],
) -> models.UP:
    try:
        parsed_id = user_manager.parse_id(id)
        return await user_manager.get(parsed_id)
    except (exceptions.UserNotExists, exceptions.InvalidID) as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND) from e


@router.get(
    path="/me",
    response_model=UserOut,
    name="get_me",
    dependencies=[Depends(get_current_active_verified_user)],
)
async def get_me(
    user: Annotated[models.UP, Depends(get_current_active_user)],
) -> User:
    return user


@router.get(
    path="/",
    response_model=list[UserOut],
    name="list_users",
    dependencies=[Depends(get_current_active_verified_superuser)],
)
async def list_users(
    db_session: Annotated[AsyncSession, Depends(get_async_session)],
) -> Sequence[User]:
    select_query = select(User)
    results = await db_session.execute(select_query)
    users_all = results.scalars().all()
    if users_all is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Keine User vorhanden",
        )

    return users_all


@router.patch(
    path="/me",
    response_model=UserOut,
    name="update_me",
)
async def update_me(
    request: Request,
    user_update: Annotated[
        UpdateUserIn, Body(..., description="Informationen des Users")
    ],
    current_user: Annotated[User, Depends(get_current_active_verified_user)],
    user_manager: Annotated[
        BaseUserManager[models.UP, models.ID], Depends(fastapi_users.get_user_manager)
    ],
) -> User:
    try:
        user_update.email = user_update.email.lower()
        update = UpdateUserDB(
            **user_update.model_dump(exclude_unset=True, exclude_none=True),
        )
        updated_user = await user_manager.update(
            update, current_user, safe=True, request=request
        )
        return updated_user
    except exceptions.InvalidPasswordException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": ErrorCode.UPDATE_USER_INVALID_PASSWORD,
                "reason": e.reason,
            },
        )
    except exceptions.UserAlreadyExists:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail="Diese Email-Adresse wird bereits verwendet",
        )


@router.get(
    "/{id}",
    response_model=UserOut,
    dependencies=[Depends(get_current_active_verified_superuser)],
    name="get_user_by_id",
)
async def get_user_by_id(user: Annotated[User, Depends(get_user_or_404)]) -> User:
    return user


@router.patch(
    "/{id}",
    response_model=UserOut,
    name="update_user",
)
async def update_user(
    user_update: Annotated[
        UpdateUserIn, Body(..., description="Informationen des Users")
    ],
    request: Request,
    user: Annotated[User, Depends(get_user_or_404)],
    current_user: Annotated[User, Depends(get_current_active_verified_superuser)],
    user_manager: Annotated[
        BaseUserManager[models.UP, models.ID], Depends(fastapi_users.get_user_manager)
    ],
) -> User:
    if user.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "reason": "Der eigene administrative Account kann nicht geändert werden",
            },
        )
    if user_update.password:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "reason": "Passwörter dürfen nicht geändert werden",
            },
        )
    try:
        user_update.email = user_update.email.lower()
        update = UpdateUserDB(
            **user_update.model_dump(
                exclude={"password"}, exclude_unset=True, exclude_none=True
            ),
        )
        user = await user_manager.update(update, user, safe=False, request=request)
        return user
    except exceptions.InvalidPasswordException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": ErrorCode.UPDATE_USER_INVALID_PASSWORD,
                "reason": e.reason,
            },
        )
    except exceptions.UserAlreadyExists:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail="Diese Email-Adresse wird bereits verwendet",
        )


@router.delete(
    "/me",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    name="delete_me",
)
async def delete_me(
    request: Request,
    current_user: Annotated[User, Depends(get_current_active_verified_user)],
    user_manager: Annotated[
        BaseUserManager[models.UP, models.ID], Depends(fastapi_users.get_user_manager)
    ],
):
    await user_manager.delete(current_user, request=request)


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    name="delete_user",
)
async def delete_user(
    request: Request,
    current_user: Annotated[User, Depends(get_current_active_verified_superuser)],
    user: Annotated[User, Depends(get_user_or_404)],
    user_manager: Annotated[
        BaseUserManager[models.UP, models.ID], Depends(fastapi_users.get_user_manager)
    ],
):
    if user.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "reason": "Der eigene administrative Account kann nicht gelöscht werden",
            },
        )
    await user_manager.delete(user, request=request)
