import logging

from aiogram_dialog.api.protocols import DialogManager
from aiogram_dialog.widgets.common import WhenCondition
from aiogram_dialog.widgets.text import Text
from fluentogram import TranslatorRunner

logger = logging.getLogger(__name__)


class I18nFormat(Text):
    def __init__(self, ftl_key: str, when: WhenCondition = None):
        super().__init__(when)
        self.ftl_key = ftl_key

    async def _render_text(self, data: dict, dialog_manager: DialogManager) -> str:
        i18n: TranslatorRunner = dialog_manager.middleware_data.get("i18n")

        if i18n is None:
            logger.error("TranslatorRunner object is not provided in middleware data.")
            raise RuntimeError("Missing `i18n` in middleware context.")

        value = i18n.get(self.ftl_key, **data)

        if value is None:
            logger.error("Translation ftl_key='%s' was not found.", self.ftl_key)
            raise KeyError(f'Translation ftl_key="{self.ftl_key}" not found')

        return value
