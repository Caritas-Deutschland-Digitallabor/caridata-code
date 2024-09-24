import re
from datetime import datetime, timezone
from uuid import UUID

from fastapi_users import schemas
from pydantic import BaseModel, Field, field_validator


class UserOut(schemas.BaseUser[UUID]):
    name: str
    created_at: datetime
    updated_at: datetime | None = None


class ValidateUser(BaseModel):
    name: str | None = None

    @field_validator("name", mode="after")
    @classmethod
    def check_name(cls, v: str) -> str:
        if not re.match(r"^[a-zA-Z0-9_\-]*$", v):
            raise ValueError(
                "Nur alphanumerische Charactere, Unter- und Bindestriche sind erlaubt"
            )
        return v


class RegisterUserIn(ValidateUser, schemas.BaseUserCreate):
    name: str


class CreateUserIn(RegisterUserIn):
    password: str | None = Field(None, exclude=True)


class RegisterUserDB(RegisterUserIn):
    created_at: datetime = datetime.now(timezone.utc)


class CreateUserDB(CreateUserIn):
    password: str
    is_active: bool = True
    is_superuser: bool = True
    is_verified: bool = True
    created_at: datetime = datetime.now(timezone.utc)


class UpdateUserIn(ValidateUser, schemas.BaseUserUpdate):
    pass


class UpdateUserDB(UpdateUserIn):
    updated_at: datetime = datetime.now(timezone.utc)
