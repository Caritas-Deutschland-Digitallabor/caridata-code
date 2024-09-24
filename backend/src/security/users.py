from datetime import datetime, timezone
import logging
import uuid
from re import match
from typing import AsyncGenerator, Union

from utils.send_email import send_email_template
from database.session import LocalAsyncSession
from fastapi import Depends, Request
from fastapi_users import (
    BaseUserManager,
    FastAPIUsers,
    InvalidPasswordException,
    UUIDIDMixin,
)
from fastapi_users.authentication import AuthenticationBackend, CookieTransport
from fastapi_users.authentication.strategy.db import (
    AccessTokenDatabase,
    DatabaseStrategy,
)
from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_users_db_sqlalchemy.access_token import SQLAlchemyAccessTokenDatabase
from models.user import AccessToken, User
from settings import settings
from sqlalchemy.ext.asyncio import AsyncSession

from security.schemas import RegisterUserIn, UpdateUserDB

logger = logging.getLogger(__name__)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with LocalAsyncSession() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


async def get_access_token_db(
    session: AsyncSession = Depends(get_async_session),
):
    yield SQLAlchemyAccessTokenDatabase(session, AccessToken)


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = settings.auth.reset_password_token_secret
    verification_token_secret = settings.auth.verification_token_secret

    async def validate_password(
        self,
        password: str,
        user: Union[RegisterUserIn, User],
    ) -> None:
        password_length = 12
        if len(password) < password_length:
            raise InvalidPasswordException(
                reason=f"Passwort muss mindestens {password_length} Zeichen enthalten."
            )
        if not match(r"^.*[a-z].*$", password):
            raise InvalidPasswordException(
                reason="Passwort muss mindestens einen Kleinbuchstaben enthalten."
            )
        if not match(r"^.*[A-Z].*$", password):
            raise InvalidPasswordException(
                reason="Passwort muss mindestens einen Großbuchstaben enthalten."
            )
        if not match(r"^.*[0-9].*$", password):
            raise InvalidPasswordException(
                reason="Passwort muss mindestens eine Zahl enthalten."
            )
        if not match(r"^.*[^a-zA-Z0-9].*$", password):
            raise InvalidPasswordException(
                reason="Passwort muss mindestens ein Symbol enthalten."
            )
        if user.email in password:
            raise InvalidPasswordException(reason="Passwort darf Email nicht enthalten")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Request | None = None
    ):
        reset_domain = (
            f"{settings.email.domain}"
            + f"{settings.email.domain_forgot_pwd_suffix}"
            + f"?token={token}"
        )
        try:
            await send_email_template(
                email_template="user_reset_password_email_template.html",
                sender=settings.email.sender,
                recipient=user.email,
                subject="Quick-Check Bauantrag - Password zurücksetzen",
                reset_domain=reset_domain,
                domain=settings.email.domain,
            )
        except Exception as e:
            logger.exception(e)

    async def on_after_register(self, user: User, request: Request | None = None):
        pass

    async def on_after_request_verify(
        self, user: User, token: str, request: Request | None = None
    ):
        verify_domain = (
            f"{settings.email.domain}"
            + f"{settings.email.domain_welcome_verify_suffix}"
            + f"?token={token}"
        )
        try:
            await send_email_template(
                email_template="user_welcome_verify_email_template.html",
                sender=settings.email.sender,
                recipient=user.email,
                subject="Caridata - Willkommen",
                verify_domain=verify_domain,
                domain=settings.email.domain,
            )
        except Exception as e:
            logger.exception(e)

    async def on_after_reset_password(self, user: User, request: Request | None = None):
        try:
            await self.update(
                UpdateUserDB(updated_at=datetime.now(timezone.utc), updated_by=user.id),
                user,
                request,
            )
        except Exception as e:
            logger.exception(e)


async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)


cookie_transport = CookieTransport(
    cookie_httponly=settings.auth.cookie_httponly,
    cookie_secure=settings.auth.cookie_secure,
    cookie_max_age=settings.auth.cookie_max_age,
)


def get_database_strategy(
    access_token_db: AccessTokenDatabase[AccessToken] = Depends(get_access_token_db),
) -> DatabaseStrategy:
    return DatabaseStrategy(
        access_token_db, lifetime_seconds=settings.auth.cookie_max_age
    )


auth_backend = AuthenticationBackend(
    name="db",
    transport=cookie_transport,
    get_strategy=get_database_strategy,
)

fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])
