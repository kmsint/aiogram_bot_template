import logging

from aiogram import Bot
from aiogram.enums import BotCommandScopeType
from aiogram.types import BotCommandScopeChat, CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button, ManagedRadio
from fluentogram import TranslatorHub, TranslatorRunner

from app.bot.keyboards.menu_button import get_main_menu_commands
from app.infrastructure.database.db import DB
from app.infrastructure.database.models.user import UserModel

logger = logging.getLogger(__name__)


async def set_radio_lang_default(_, dialog_manager: DialogManager):
    locales: list[str] = dialog_manager.middleware_data.get("bot_locales")
    user_row: UserModel = dialog_manager.middleware_data.get("user_row")
    item_id = str(locales.index(user_row.language) + 1)
    radio: ManagedRadio = dialog_manager.find("radio_lang")

    await radio.set_checked(item_id)


async def update_user_lang(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
):
    bot: Bot = dialog_manager.middleware_data.get("bot")
    translator_hub: TranslatorHub = dialog_manager.middleware_data.get("translator_hub")
    db: DB = dialog_manager.middleware_data.get("db")
    locales: list[str] = dialog_manager.middleware_data.get("bot_locales")
    radio_lang: ManagedRadio = dialog_manager.find("radio_lang")
    checked_locale = locales[int(radio_lang.get_checked()) - 1]
    i18n: TranslatorRunner = translator_hub.get_translator_by_locale(checked_locale)
    dialog_manager.middleware_data["i18n"] = i18n

    await db.users.update_user_lang(
        user_id=callback.from_user.id, user_lang=checked_locale
    )
    await bot.set_my_commands(
        commands=get_main_menu_commands(i18n=i18n),
        scope=BotCommandScopeChat(
            type=BotCommandScopeType.CHAT, chat_id=callback.from_user.id
        ),
    )
    await callback.answer(text=i18n.lang.saved())
    await dialog_manager.done()


async def cancel_set_lang(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.done()
