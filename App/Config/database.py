from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.config.config import get_reverse_bit_db_settings


"""
ReverseBit DB connection pooling
"""
global_auth_settings = get_reverse_bit_db_settings()
print(global_auth_settings)

reversebit_db_engine = create_async_engine(
    url=str(global_auth_settings.asyncpg_url),
    future=True,
    echo=True,
    pool_pre_ping=True,
)

AsyncReverseBitDBSessionFactory = sessionmaker(
    reversebit_db_engine, autoflush=False, expire_on_commit=False, class_=AsyncSession
)


async def get_reversebit_db() -> AsyncGenerator:
    async with AsyncReverseBitDBSessionFactory() as reversebit_db_session:
        yield reversebit_db_session
