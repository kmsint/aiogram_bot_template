import logging
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User
from fluentogram import TranslatorHub

from app.infrastructure.database.models.user import UserModel

logger = logging.getLogger(__name__)


class TranslatorRunnerMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        user: User = data.get("event_from_user")

        if user is None:
            return await handler(event, data)

        user_row: UserModel = data.get("user_row")

        if user_row and user_row.language:
            user_lang = user_row.language
        else:
            user_lang = user.language_code

        hub: TranslatorHub = data.get("translator_hub")
        data["i18n"] = hub.get_translator_by_locale(user_lang)

        return await handler(event, data)
