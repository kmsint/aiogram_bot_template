import logging

from typing import Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import Update
from asyncpg import Pool, exceptions

from app.infrastructure.database.database.db import DB

logger = logging.getLogger(__name__)


class DataBaseMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Update, dict[str, any]], Awaitable[None]],
        event: Update,
        data: dict[str, any]
    ) -> any:
        pool: Pool = data.get('_db_pool')

        async with pool.acquire() as connection:
            async with connection.transaction():
                try:
                    data['db'] = DB(connection)
                    result = await handler(event, data)
                except exceptions.PostgresError as e:
                    logger.exception('Transaction rolled back due to error: %s', e)
                    result = await handler(event, data)

        return result