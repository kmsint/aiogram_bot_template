import logging
from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Update, User
from app.infrastructure.database.models.user import UserModel

logger = logging.getLogger(__name__)


class ShadowBanMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: dict[str, Any],
    ) -> Any:
        user_row: UserModel | None = data.get("user_row")
        if user_row is None:
            logger.warning(
                "Cannot check for shadow ban. The 'user_row' "
                "key was not found in the middleware data."
            )
            return await handler(event, data)

        if user_row.banned:
            logger.warning("Shadow-banned user tried to interact: %d", user_row.user_id)
            if event.callback_query:
                await event.callback_query.answer()
            return

        return await handler(event, data)
