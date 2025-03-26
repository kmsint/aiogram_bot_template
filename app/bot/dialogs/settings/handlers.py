import logging

from aiogram.types import CallbackQuery, User
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button, ManagedRadio
from fluentogram import TranslatorHub, TranslatorRunner

from app.infrastructure.database.database.db import DB
from app.infrastructure.database.models.users import UsersModel

logger = logging.getLogger(__name__)


async def set_radio_lang_default(_, dialog_manager: DialogManager):
    user: User = dialog_manager.middleware_data.get("event_from_user")
    locales: list[str] = dialog_manager.middleware_data.get("bot_locales")
    db: DB = dialog_manager.middleware_data.get("db")
    user_record: UsersModel = await db.users.get_user_record(user_id=user.id)
    item_id = str(locales.index(user_record.language) + 1)
    radio: ManagedRadio = dialog_manager.find("radio_lang")

    await radio.set_checked(item_id)


async def update_user_lang(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
):
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
    await callback.answer(text=i18n.lang.saved())
    await dialog_manager.done()


async def cancel_set_lang(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.done()
