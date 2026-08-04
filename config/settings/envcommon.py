from typing import Any 

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class CommonEnvSettings(BaseSettings):
    SECRET_KEY: str = Field(default="django-insecure-change-this-in-production")
    DEBUG: bool = Field(default=False)
    ENVIRONMENT: str = Field(default="local")
    ALLOWED_HOSTS: list[str] = Field(default=["localhost", "127.0.0.1"])

    LANGUAGE_CODE: str = Field(default="en-us")
    TIME_ZONE: str = Field(default="Asia/Jakarta")

    EMAIL_BACKEND: str = Field(default="django.core.mail.backends.console.EmailBackend")
    EMAIL_HOST: str = Field(default="localhost")
    EMAIL_PORT: int = Field(default=587)
    EMAIL_USE_TLS: bool = Field(default=True)
    EMAIL_HOST_USER: str = Field(default="")
    EMAIL_HOST_PASSWORD: str = Field(default="")

    model_config = SettingsConfigDict(
        env_prefix="DJANGO_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @field_validator("ALLOWED_HOSTS", mode="before")
    @classmethod
    def split_allowed_hosts(cls, v: Any) -> Any:
        if isinstance(v, str) and not v.startswith("["):
            return [h.strip() for h in v.split(",") if h.strip()]
        return v

    @field_validator("SECRET_KEY", mode="after")
    @classmethod
    def enforce_secret_key_in_prod(cls, v: str, info) -> str:
        if info.data.get("ENVIRONMENT") not in ("local", "test") and v.startswith("django-insecure"):
            raise ValueError("SECRET_KEY must be explicitly set outside local/test.")
        return v

    # Helper Properties for Django settings
    @property
    def secret_key(self) -> str:
        return self.SECRET_KEY
    @property
    def debug(self) -> str:
        return self.DEBUG
    
    @property
    def environment(self) -> str:
        return self.ENVIRONMENT
    
    @property
    def allowed_hosts(self) -> str:
        return self.ALLOWED_HOSTS
    
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
    def email_port(self) -> str:
        return self.EMAIL_PORT
    
    @property
    def email_use_tls(self) -> str:
        return self.EMAIL_USE_TLS
    
    @property
    def email_host_user(self) -> str:
        return self.EMAIL_HOST_USER
    
    @property
    def email_host_password(self) -> str:
        return self.EMAIL_HOST_PASSWORD
