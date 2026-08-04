from typing import Any 

from pydantic import Field, field_validator, Json
from pydantic_settings import BaseSettings, SettingsConfigDict

class CommonEnvSettings(BaseSettings):
    SECRET_KEY: str = Field(
        default="django-insecure-change-this-in-production",
        description="Django secret key for cryptographic signing",
    )
    
    DEBUG: bool = Field(default=False, description="Enable debug mode")
    ENVIRONMENT: str = Field(default="local", description="Current environment (local, dev, prod)")

    ALLOWED_HOSTS: list[str] = Field(
        default=["localhost", "127.0.0.1"],
        description="List of allowed host/domain names",
    )

    LANGUAGE_CODE: str = Field(default="en-us", description="Language code for the application")
    TIME_ZONE: str = Field(default="Asia/Jakarta", description="Time zone for the application")

    EMAIL_BACKEND: str = Field(
        default="django.core.mail.backends.console.EmailBackend", 
        description="Email backend to use"
    )
    EMAIL_HOST: str = Field(default="localhost", description="Email server host")
    EMAIL_PORT: str = Field(default="587", description="Email server port")
    EMAIL_USE_TLS: str = Field(default="True", description="Use TLS for email")
    EMAIL_HOST_USER: str = Field(default="", description="Email server username")
    EMAIL_HOST_PASSWORD: str = Field(default="", description="Email server password")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @field_validator("SECRET_KEY", mode="before")
    @classmethod
    def empty_secret_key_to_default(cls, v: Any) -> Any:
        if v == "" or v is None:
            return "django-insecure-change-this-in-production"
        return v

    @field_validator("ALLOWED_HOSTS", mode="before")
    @classmethod
    def validate_allowed_hosts(cls, v):
        if isinstance(v, str):
            parsed = Json.loads(v)
        
            if parsed == []:
                return ["localhost", "127.0.0.1"]
            return parsed
        
        if isinstance(v, list) and v == []:
            return ["localhost", "127.0.0.1"]
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
