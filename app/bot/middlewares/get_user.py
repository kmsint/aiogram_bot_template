import logging
from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import Update, User

from app.infrastructure.database.db import DB
from app.infrastructure.database.models.user import UserModel

logger = logging.getLogger(__name__)


class GetUserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Update, dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: dict[str, Any],
    ) -> Any:
        user: User = data.get("event_from_user")

        if user is None:
            return await handler(event, data)

        db: DB = data.get("db")

        if db is None:
            logger.error("Database object is not provided in middleware data.")
            raise RuntimeError("Missing `db` in middleware context.")

        user_row: UserModel | None = await db.users.get_user(user_id=user.id)

        data.update(user_row=user_row)

        return await handler(event, data)
