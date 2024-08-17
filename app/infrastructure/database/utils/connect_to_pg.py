import logging

from psycopg_pool import AsyncConnectionPool

logger = logging.getLogger(__name__)


async def get_pg_pool(
    db_name: str,
    host: str,
    port: int,
    user: str,
    password: str,
) -> AsyncConnectionPool:
    dp_pool = AsyncConnectionPool(
        conninfo=f'postgresql://{user}:{password}@{host}:{port}/{db_name}',
        min_size=1,
        max_size=3,
    )
    # version = await db_pool.connection(). fetchone("SELECT version() as ver;")
    # logger.info(f"Connected to {version['ver']}")
    await dp_pool.open()

    return dp_pool
