from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class TableName(BaseSettings):
    board_game: str
    model_config = SettingsConfigDict(env_prefix='TABLE_NAME_')


@lru_cache
def table_name():
    return TableName()  # pyright: ignore[reportCallIssue]
