from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode
from fluentogram import TranslatorRunner

from app.services.delay_service.publisher import delay_message_deletion
from app.tgbot.states.start import StartSG
from nats.js.client import JetStreamContext
from app.services.scheduler.task_scheduler import my_task
from app.infrastructure.database.database.db import DB
from app.infrastructure.database.models.users import UsersModel
from app.tgbot.enums.roles import UserRole

commands_router = Router()


@commands_router.message(CommandStart())
async def process_start_command(
    message: Message,
    dialog_manager: DialogManager,
    i18n: TranslatorRunner,
    db: DB
) -> None:
    user_record: UsersModel | None = await db.users.get_user_record(user_id=message.from_user.id)
    if user_record is None:
        await db.users.add(
            user_id=message.from_user.id, 
            language=message.from_user.language_code,
            role=UserRole.USER
        )
    await dialog_manager.start(state=StartSG.start, mode=StartMode.RESET_STACK)


# Этот хэндлер будет срабатывать на команду /del
@commands_router.message(Command('del'))
async def send_and_del_message(
    message: Message, 
    i18n: TranslatorRunner, 
    js: JetStreamContext, 
    delay_del_subject: str
) -> None:
    
    delay = 3
    msg: Message = await message.answer(text=i18n.will.delete(delay=delay))
    
    await delay_message_deletion(
        js=js,  
        chat_id=msg.chat.id, 
        message_id=msg.message_id,
        subject=delay_del_subject, 
        delay=delay
    )


## Simple command to handle
@commands_router.message(Command("task"))
async def message(message: Message):
    await my_task.kiq(message.chat.id)


# @commands_router.message(Command('help'))
# async def process_help_command(
#     message: Message,
#     dialog_manager: DialogManager,
#     i18n: TranslatorRunner
# ) -> None:
#     await message.answer(text=i18n.help.command())
