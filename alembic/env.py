import asyncio
from logging.config import fileConfig

from sqlalchemy.ext.asyncio import AsyncConnection, create_async_engine

from alembic import context
from app.config.loader import get_config

# Alembic Config object
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata object for autogenerate support (if needed, otherwise None)
target_metadata = None

# Database URL for SQLAlchemy
app_config = get_config()
url = f"postgresql+psycopg://{app_config.postgres.user}:{app_config.postgres.password}@{app_config.postgres.host}:{app_config.postgres.port}/{app_config.postgres.name}"
engine = create_async_engine(url)


async def run_migrations():
    async with engine.connect() as connection:
        await connection.run_sync(do_run_migrations)


def do_run_migrations(connection: AsyncConnection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        render_as_batch=True,
    )

    with context.begin_transaction():
        context.run_migrations()


asyncio.run(run_migrations())
