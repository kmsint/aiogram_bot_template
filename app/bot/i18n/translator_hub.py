from fluent_compiler.bundle import FluentBundle
from fluentogram import FluentTranslator, TranslatorHub

from config.config import settings

DIR_PATH = "locales"


def create_translator_hub() -> TranslatorHub:
    translator_hub = TranslatorHub(
        {"ru": ("ru", "en"), "en": ("en", "ru")},
        [
            FluentTranslator(
                locale="ru",
                translator=FluentBundle.from_files(
                    locale="ru-RU", filenames=[f"{DIR_PATH}/ru/LC_MESSAGES/txt.ftl"]
                ),
            ),
            FluentTranslator(
                locale="en",
                translator=FluentBundle.from_files(
                    locale="en-US", filenames=[f"{DIR_PATH}/en/LC_MESSAGES/txt.ftl"]
                ),
            ),
        ],
        root_locale=settings.i18n.default_locale,
    )
    return translator_hub
