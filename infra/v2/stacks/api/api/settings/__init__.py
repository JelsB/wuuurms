from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class TableName(BaseSettings):
    board_game: str
    model_config = SettingsConfigDict(env_prefix='TABLE_NAME_')


@lru_cache
def table_name():
    return TableName()  # pyright: ignore[reportCallIssue]


class CommonEnvVars(BaseSettings):
    environment: str


@lru_cache
def common_env_vars():
    return CommonEnvVars()  # pyright: ignore[reportCallIssue]


class LocalEnvVars(BaseSettings):
    api_id: str | None = None
    model_config = SettingsConfigDict(env_prefix='LOCAL_')


@lru_cache
def local_env_vars():
    return LocalEnvVars()  # pyright: ignore[reportCallIssue]
