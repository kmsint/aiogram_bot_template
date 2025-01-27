from fluent_compiler.bundle import FluentBundle
from fluentogram import FluentTranslator, TranslatorHub

from config.config import settings


def create_translator_hub() -> TranslatorHub:
    translator_hub = TranslatorHub(
        {
            "ru": ("ru", "en"),
            "en": ("en", "ru")
        },
        [
            FluentTranslator(
                locale="ru",
                translator=FluentBundle.from_files(
                    locale="ru-RU",
                    filenames=["locales/ru/LC_MESSAGES/txt.ftl"])),
            FluentTranslator(
                locale="en",
                translator=FluentBundle.from_files(
                    locale="en-US",
                    filenames=["locales/en/LC_MESSAGES/txt.ftl"]))
        ],
        root_locale=settings.i18n.default_locale
    )
    return translator_hub