from typing import Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import Update
from asyncpg import Pool

from app.infrastructure.database.database.db import DB


class DataBaseMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Update, dict[str, any]], Awaitable[None]],
        event: Update,
        data: dict[str, any]
    ) -> any:
        pool: Pool = data.get('_db_pool')

        async with pool.acquire() as connect:
            data['db'] = DB(connect)

            await handler(event, data)