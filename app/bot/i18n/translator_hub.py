from pathlib import Path

from fluent_compiler.bundle import FluentBundle
from fluentogram import FluentTranslator, TranslatorHub

from app.services.parsers.file_names_parser import list_file_paths_in_dir


def create_translator_hub(
    locales_directory: Path | str,
    locales_map: dict[str, list[str]],
    default_locale: str,
) -> TranslatorHub:
    translator_hub = TranslatorHub(
        locales_map=locales_map,
        translators=[
            FluentTranslator(
                locale="ru",
                translator=FluentBundle.from_files(
                    locale="ru-RU",
                    filenames=list_file_paths_in_dir(
                        directory=f"{locales_directory}/locales/ru/LC_MESSAGES/"
                    ),
                    use_isolating=False,
                ),
            ),
            FluentTranslator(
                locale="en",
                translator=FluentBundle.from_files(
                    locale="en-US",
                    filenames=list_file_paths_in_dir(
                        directory=f"{locales_directory}/locales/en/LC_MESSAGES/"
                    ),
                    use_isolating=False,
                ),
            ),
        ],
        root_locale=default_locale,
    )
    return translator_hub
