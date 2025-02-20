import logging

from typing import Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Update

logger = logging.getLogger(__name__)


class SetLangMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[CallbackQuery, dict[str, any]], Awaitable[None]],
        event: Update,
        data: dict[str, any]
    ) -> any:

        return await handler(event, data)