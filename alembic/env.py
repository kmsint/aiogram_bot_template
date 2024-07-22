import asyncio
from logging.config import fileConfig

from sqlalchemy.ext.asyncio import AsyncConnection, create_async_engine

from alembic import context
from app.tgbot.config.config import PostgresConfig, load_pg_config

# Alembic Config object
config = context.config
config_pg: PostgresConfig = load_pg_config()

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata object for autogenerate support (if needed, otherwise None)
target_metadata = None

# Database URL for SQLAlchemy
url = f"postgresql+asyncpg://{config_pg.username}:{config_pg.password}@{config_pg.host}:{config_pg.port}/{config_pg.db_name}"
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
