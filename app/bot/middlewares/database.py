import logging
from typing import Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import Update
from psycopg import Error
from psycopg_pool import AsyncConnectionPool

from app.infrastructure.database.database.db import DB

logger = logging.getLogger(__name__)


class DataBaseMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Update, dict[str, any]], Awaitable[None]],
        event: Update,
        data: dict[str, any],
    ) -> any:
        db_pool: AsyncConnectionPool = data.get("_db_pool")

        async with db_pool.connection() as connection:
            async with connection.transaction():
                try:
                    data["db"] = DB(connection)
                    result = await handler(event, data)
                except Error as e:
                    logger.exception("Transaction rolled back due to error: %s", e)
                    result = await handler(event, data)

        return result
