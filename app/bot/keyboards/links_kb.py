from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from fluentogram import TranslatorRunner


def get_links_kb(i18n: TranslatorRunner) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=i18n.about.author(), url=i18n.about.author.link()
                )
            ],
            [
                InlineKeyboardButton(
                    text=i18n.free.course(), url=i18n.free.course.link()
                )
            ],
            [
                InlineKeyboardButton(
                    text=i18n.advanced.course(), url=i18n.advanced.course.link()
                )
            ],
            [InlineKeyboardButton(text=i18n.mlpodcast(), url=i18n.mlpodcast.link())],
        ]
    )
