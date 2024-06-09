from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import PostgresDsn
from .constant import (
    DATABASE_HOST,
    DATABASE_USER_NAME,
    DATABASE_PASSWORD,
    DATABASE,
    DATABASE_PORT,
    DB_TYPE,
)


class ReverseBitDBSettings(BaseSettings):
    asyncpg_url: PostgresDsn = PostgresDsn.build(
        scheme=DB_TYPE,
        username=DATABASE_USER_NAME,
        password=DATABASE_PASSWORD,
        host=DATABASE_HOST,
        port=int(DATABASE_PORT),
        path=DATABASE,
    )


@lru_cache
def get_reverse_bit_db_settings():
    return ReverseBitDBSettings()


reverse_bit_db_setting = get_reverse_bit_db_settings()
