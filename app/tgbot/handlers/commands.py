from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode
from fluentogram import TranslatorRunner

from app.tgbot.states.start import StartSG

commands_router = Router()


@commands_router.message(CommandStart())
async def process_start_command(
    message: Message,
    dialog_manager: DialogManager,
    i18n: TranslatorRunner
) -> None:
    await dialog_manager.start(state=StartSG.start, mode=StartMode.RESET_STACK)


# @commands_router.message(Command('help'))
# async def process_help_command(
#     message: Message,
#     dialog_manager: DialogManager,
#     i18n: TranslatorRunner
# ) -> None:
#     await message.answer(text=i18n.help.command())
