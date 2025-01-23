from datetime import datetime, timedelta, timezone

from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode
from fluentogram import TranslatorRunner
from taskiq_redis import RedisScheduleSource

from app.infrastructure.database.database.db import DB
from app.infrastructure.database.models.users import UsersModel
from app.services.delay_service.publisher import delay_message_deletion
from app.services.scheduler.tasks import (
    dynamic_periodic_task,
    scheduled_task,
    simple_task,
)
from app.tgbot.enums.roles import UserRole
from app.tgbot.keyboards.links_kb import get_links_kb
from app.tgbot.states.start import StartSG
from nats.js.client import JetStreamContext

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


@commands_router.message(Command('simple'))
async def task_handler(
    message: Message, 
    i18n: TranslatorRunner, 
    redis_source: RedisScheduleSource
) -> None:
    await simple_task.kiq()
    await message.answer(text=i18n.simple.task())


@commands_router.message(Command('delay'))
async def delay_task_handler(
    message: Message, 
    i18n: TranslatorRunner, 
    redis_source: RedisScheduleSource
) -> None:
    await scheduled_task.schedule_by_time(
        source=redis_source, 
        time=datetime.now(timezone.utc) + timedelta(seconds=5)
    )
    await message.answer(text=i18n.task.soon())


@commands_router.message(Command('periodic'))
async def dynamic_periodic_task_handler(
    i18n: TranslatorRunner, 
    message: Message, redis_source: RedisScheduleSource
) -> None:
    await dynamic_periodic_task.schedule_by_cron(
        source=redis_source, 
        cron='*/2 * * * *'
    )
    await message.answer(text=i18n.periodic.task())


@commands_router.message(Command('help'))
async def process_help_command(
    message: Message,
    dialog_manager: DialogManager,
    i18n: TranslatorRunner
) -> None:
    await message.answer(
        text=i18n.help.command(),
        reply_markup=get_links_kb(i18n=i18n)
    )
