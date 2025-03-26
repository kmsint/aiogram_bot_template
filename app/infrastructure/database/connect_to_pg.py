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
    try:
        db_pool = AsyncConnectionPool(
            conninfo=f"postgresql://{user}:{password}@{host}:{port}/{db_name}",
            min_size=1,
            max_size=3,
            open=False,
        )

        await db_pool.open()

        async with db_pool.connection() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("SELECT version();")
                db_version = await cursor.fetchone()
                logger.info(f"Connected to {db_version[0]}")
        return db_pool
    except Exception as e:
        logger.exception(
            "Something went wrong while connecting to the database with exception: %s",
            e,
        )
        raise
