from typing import Annotated, Any

from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict


class CommonEnvSettings(BaseSettings):
    SECRET_KEY: str = Field(default="django-insecure-change-this-in-production")
    DEBUG: bool = Field(default=False)
    ENVIRONMENT: str = Field(default="local")
    ALLOWED_HOSTS: Annotated[list[str], NoDecode] = Field(default=["localhost", "127.0.0.1"])
    CSRF_TRUSTED_ORIGINS: Annotated[list[str], NoDecode] = Field(default=[])

    LOG_LEVEL: str = Field(default="INFO")
    LANGUAGE_CODE: str = Field(default="en-us")
    TIME_ZONE: str = Field(default="Asia/Jakarta")

    EMAIL_BACKEND: str = Field(default="django.core.mail.backends.console.EmailBackend")
    EMAIL_HOST: str = Field(default="localhost")
    EMAIL_PORT: int = Field(default=587)
    EMAIL_USE_TLS: bool = Field(default=True)
    EMAIL_HOST_USER: str = Field(default="")
    EMAIL_HOST_PASSWORD: str = Field(default="")

    model_config = SettingsConfigDict(
        env_prefix="COMMON_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @field_validator("ALLOWED_HOSTS", "CSRF_TRUSTED_ORIGINS", mode="before")
    @classmethod
    def split_csv(cls, v: Any) -> Any:
        if isinstance(v, str):
            return [h.strip() for h in v.split(",") if h.strip()]
        return v

    @model_validator(mode="after")
    def enforce_secret_key_in_prod(self) -> CommonEnvSettings:
        if self.ENVIRONMENT not in ("local", "test") and self.SECRET_KEY.startswith("django-insecure"):
            raise ValueError("SECRET_KEY must be explicitly set outside local/test.")
        return self

    # Helper properties (lower_snake_case) for readability at call sites.
    @property
    def secret_key(self) -> str:
        return self.SECRET_KEY

    @property
    def debug(self) -> bool:
        return self.DEBUG

    @property
    def environment(self) -> str:
        return self.ENVIRONMENT

    @property
    def allowed_hosts(self) -> list[str]:
        return self.ALLOWED_HOSTS

    @property
    def csrf_trusted_origins(self) -> list[str]:
        return self.CSRF_TRUSTED_ORIGINS

    @property
    def log_level(self) -> str:
        return self.LOG_LEVEL

    @property
    def language_code(self) -> str:
        return self.LANGUAGE_CODE

    @property
    def timezone(self) -> str:
        return self.TIME_ZONE

    @property
    def email_backend(self) -> str:
        return self.EMAIL_BACKEND

    @property
    def email_host(self) -> str:
        return self.EMAIL_HOST

    @property
    def email_port(self) -> int:
        return self.EMAIL_PORT

    @property
    def email_use_tls(self) -> bool:
        return self.EMAIL_USE_TLS

    @property
    def email_host_user(self) -> str:
        return self.EMAIL_HOST_USER

    @property
    def email_host_password(self) -> str:
        return self.EMAIL_HOST_PASSWORD
