from enum import StrEnum
from pathlib import Path
from typing import Annotated, Any

from pydantic import BaseModel, Field, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


DEFAULT_SQLITE_PATH = (Path(__file__).resolve().parent.parent.parent / "db.sqlite3").as_posix()


class DBEngineEnum(StrEnum):
    SQLITE = "django.db.backends.sqlite3"
    POSTGRES = "django.db.backends.postgresql"


class BaseDatabaseSettings(BaseSettings):
    engine: DBEngineEnum = Field(
        default=DBEngineEnum.SQLITE,
        serialization_alias="ENGINE",
    )

    model_config = SettingsConfigDict(
        env_prefix="DATABASE_",
        extra="ignore",
        frozen=True,
        env_ignore_empty=True,
        populate_by_name=True,
        env_file=".env",
    )

    @field_validator("engine", mode="before")
    @classmethod
    def resolve_engine_alias(cls, v: Any) -> Any:
        if isinstance(v, str):
            try:
                return DBEngineEnum[v.upper()]
            except KeyError:
                pass
        return v


class SqliteDatabaseSettings(BaseDatabaseSettings):
    engine: DBEngineEnum = Field(
        default=DBEngineEnum.SQLITE,
        serialization_alias="ENGINE",
    )
    name: str = Field(
        default=DEFAULT_SQLITE_PATH,
        serialization_alias="NAME",
    )


class PostgresDatabaseSettings(BaseDatabaseSettings):
    engine: DBEngineEnum = Field(
        default=DBEngineEnum.POSTGRES,
        serialization_alias="ENGINE",
    )
    host: str = Field(
        default="localhost",
        serialization_alias="HOST",
    )
    port: int = Field(
        default=5432,
        gt=0,
        le=65535,
        serialization_alias="PORT",
    )
    name: str = Field(
        default="forma",
        serialization_alias="NAME",
    )
    user: str = Field(serialization_alias="USER")
    password: SecretStr = Field(serialization_alias="PASSWORD")


class DjangoDatabases(BaseModel):
    default: Annotated[
        PostgresDatabaseSettings | SqliteDatabaseSettings,
        Field(discriminator="engine"),
    ]
    
