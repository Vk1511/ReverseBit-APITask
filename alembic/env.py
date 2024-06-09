import asyncio
from alembic import context
from sqlalchemy.ext.asyncio import create_async_engine
from app.config.config import reverse_bit_db_setting
from app.models.base import Base
from app.models.employee import Company, UserCompany
from app.models.auth import User

target_metadata = Base.metadata


def do_run_migrations(connection):
    context.configure(
        compare_type=True,
        dialect_opts={"paramstyle": "named"},
        connection=connection,
        target_metadata=target_metadata,
        include_schemas=True,
        # literal_binds=True,
        version_table_schema=target_metadata.schema,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = create_async_engine(
        str(reverse_bit_db_setting.asyncpg_url), future=True
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)


asyncio.run(run_migrations_online())
