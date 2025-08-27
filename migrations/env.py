from __future__ import annotations

import asyncio
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from alembic import context

from src.utils.db import Base
from src.user.models import User  # ensure models are imported
from src.config import settings


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


target_metadata = Base.metadata


def get_url() -> str:
    return (
        f"postgresql+asyncpg://{settings.database_user}:{settings.database_password}"
        f"@{settings.database_host}:{settings.database_port}/{settings.database_name}"
    )


def run_migrations_offline() -> None:
    url = get_url()
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    connectable = context.config.attributes.get("connection", None)
    if connectable is None:
        from sqlalchemy.ext.asyncio import create_async_engine

        connectable = create_async_engine(get_url(), poolclass=pool.NullPool)

    async with connectable.connect() as connection:  # type: ignore[reportGeneralTypeIssues]
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()  # type: ignore[reportGeneralTypeIssues]


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())


