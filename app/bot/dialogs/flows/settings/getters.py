from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import ManagedRadio
from fluentogram import TranslatorHub, TranslatorRunner

from app.bot.dialogs.flows.settings.keyboards import get_lang_buttons


async def get_set_lang(dialog_manager: DialogManager, i18n: TranslatorRunner, **kwargs):
    locales = dialog_manager.middleware_data.get("bot_locales")
    translator_hub: TranslatorHub = dialog_manager.middleware_data.get("translator_hub")
    radio_lang: ManagedRadio = dialog_manager.find("radio_lang")
    checked_locale = locales[int(radio_lang.get_checked()) - 1]
    i18n: TranslatorRunner = translator_hub.get_translator_by_locale(checked_locale)

    return {
        "set_lang": i18n.set.lang.menu(),
        "lang_buttons": get_lang_buttons(locales=locales, i18n=i18n),
        "back_button": i18n.back.button(),
        "save_button": i18n.save.button(),
    }
