import logging
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.fsm.context import FSMContext
from aiogram.types import TelegramObject, User
from fluentogram import TranslatorHub

from app.infrastructure.database.database.db import DB

logger = logging.getLogger(__name__)


class TranslatorRunnerMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:

        user: User = data.get('event_from_user')

        if user is None:
            return await handler(event, data)

        state: FSMContext = data.get('state')
        user_data = await state.get_data()
        db: DB = data.get('db')

        if user_data.get('user_lang'):
            user_lang = user_data['user_lang']
        elif (user_row := await db.users.get_user_record(
            user_id=user.id)) and user_row.language:
            user_lang = user_row.language
        else:
            user_lang = user.language_code

        hub: TranslatorHub = data.get('_translator_hub')
        data['i18n'] = hub.get_translator_by_locale(user_lang)

        return await handler(event, data)