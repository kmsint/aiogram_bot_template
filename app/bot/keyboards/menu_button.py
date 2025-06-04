import logging

from aiogram.types import BotCommand
from fluentogram import TranslatorRunner

logger = logging.getLogger(__name__)


def get_main_menu_commands(i18n: TranslatorRunner):
    menu_commands = {
        "/start": i18n.start.command.description(),
        "/lang": i18n.lang.command.description(),
        "/help": i18n.help.command.description(),
    }
    main_menu_commands = [
        BotCommand(command=command, description=description)
        for command, description in menu_commands.items()
    ]
    return main_menu_commands
