import re
from typing import Literal

from pydantic import BaseModel, EmailStr, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

ENVIRONMENT_LITERAL = Literal["LOCAL", "DEVELOPMENT", "PRODUCTION"]


class EnvironmentSettings(BaseModel):
    environment: ENVIRONMENT_LITERAL = "LOCAL"


class DatabaseSettings(BaseModel):
    host: str
    port: int = 5432
    user: str
    password: str
    database: str

    @property
    def dsn(self) -> str:
        return (
            "postgresql+asyncpg://"
            f"{self.user}:{self.password}"
            f"@{self.host}:{self.port}/{self.database}"
        )


class CorsSettings(BaseModel):
    allow_origins: list[str] = ["http://localhost:3000"]
    allow_credentials: bool = True
    allow_methods: list[str] = ["*"]
    allow_headers: list[str] = ["*"]


class CSRFSettings(BaseModel):
    secret: str
    cookie_name: str = "caridata_csrf_token"
    cookie_domain: str | None = None
    cookie_secure: bool = False
    cookie_samesite: str = "lax"
    header_name: str = "x-csrf-token"
    exempt_urls: list[re.Pattern] | None = None


class AuthSettings(BaseModel):
    reset_password_token_secret: str
    verification_token_secret: str
    cookie_secure: bool
    cookie_httponly: bool = True
    cookie_max_age: int = 60 * 60 * 24 * 180  # 180 days


class EmailSettings(BaseModel):
    sender: EmailStr
    domain: HttpUrl
    domain_forgot_pwd_suffix: str
    domain_invite_pwd_suffix: str
    domain_welcome_verify_suffix: str


class ScalewaySettings(BaseModel):
    project_id: str
    api_token: str


class CaritasSettings(BaseModel):
    api_uri: HttpUrl
    api_category: int = 58149
    api_basic_auth_username: EmailStr
    api_basic_auth_password: str


class Settings(BaseSettings):
    environment: EnvironmentSettings
    database: DatabaseSettings
    cors: CorsSettings
    csrf: CSRFSettings
    auth: AuthSettings
    email: EmailSettings
    scaleway: ScalewaySettings
    caritas: CaritasSettings

    model_config = SettingsConfigDict(
        env_prefix="API_",
        case_sensitive=False,
        env_nested_delimiter="__",
        env_file=".env",
    )


settings = Settings()
