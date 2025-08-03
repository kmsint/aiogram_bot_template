from datetime import datetime, timedelta, timezone

from aiogram import Bot, Router
from aiogram.enums import BotCommandScopeType
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import BotCommandScopeChat, Message
from aiogram_dialog import DialogManager, StartMode
from fluentogram import TranslatorRunner
from taskiq import ScheduledTask
from taskiq_redis import RedisScheduleSource

from app.bot.enums.roles import UserRole
from app.bot.filters.dialog_filters import DialogStateFilter, DialogStateGroupFilter
from app.bot.keyboards.links_kb import get_links_kb
from app.bot.dialogs.flows.settings.states import SettingsSG
from app.bot.dialogs.flows.start.states import StartSG
from app.bot.keyboards.menu_button import get_main_menu_commands
from app.infrastructure.database.db import DB
from app.infrastructure.database.models.user import UserModel
from app.services.delay_service.publisher import delay_message_deletion
from app.services.scheduler.tasks import (
    dynamic_periodic_task,
    scheduled_task,
    simple_task,
)
from nats.js.client import JetStreamContext

commands_router = Router()


@commands_router.message(CommandStart())
async def process_start_command(
    message: Message,
    dialog_manager: DialogManager,
    bot: Bot,
    i18n: TranslatorRunner,
    db: DB,
    user_row: UserModel | None,
) -> None:
    if user_row is None:
        await db.users.add(
            user_id=message.from_user.id,
            language=message.from_user.language_code,
            role=UserRole.USER,
        )
    await bot.set_my_commands(
        commands=get_main_menu_commands(i18n=i18n),
        scope=BotCommandScopeChat(
            type=BotCommandScopeType.CHAT, chat_id=message.from_user.id
        ),
    )
    await dialog_manager.start(state=StartSG.start, mode=StartMode.RESET_STACK)


# Этот хэндлер будет срабатывать на команду /del
@commands_router.message(Command("del"))
async def send_and_del_message(
    message: Message,
    i18n: TranslatorRunner,
    js: JetStreamContext,
    delay_del_subject: str,
) -> None:
    delay = 3
    msg: Message = await message.answer(text=i18n.will.delete(delay=delay))

    await delay_message_deletion(
        js=js,
        chat_id=msg.chat.id,
        message_id=msg.message_id,
        subject=delay_del_subject,
        delay=delay,
    )


@commands_router.message(Command("simple"))
async def task_handler(
    message: Message, i18n: TranslatorRunner, redis_source: RedisScheduleSource
) -> None:
    await simple_task.kiq()
    await message.answer(text=i18n.simple.task())


@commands_router.message(Command("delay"))
async def delay_task_handler(
    message: Message, i18n: TranslatorRunner, redis_source: RedisScheduleSource
) -> None:
    await scheduled_task.schedule_by_time(
        source=redis_source, time=datetime.now(timezone.utc) + timedelta(seconds=5)
    )
    await message.answer(text=i18n.task.soon())


@commands_router.message(Command("periodic"))
async def dynamic_periodic_task_handler(
    message: Message,
    i18n: TranslatorRunner,
    state: FSMContext,
    redis_source: RedisScheduleSource,
) -> None:
    periodic_task: ScheduledTask = await dynamic_periodic_task.schedule_by_cron(
        source=redis_source, cron="*/2 * * * *"
    )

    data: dict = await state.get_data()
    if data.get("periodic_tasks") is None:
        data["periodic_tasks"] = []

    data["periodic_tasks"].append(periodic_task.schedule_id)

    await state.set_data(data)

    await message.answer(text=i18n.periodic.task())


@commands_router.message(Command("del_periodic"))
async def delete_all_periodic_tasks_handler(
    message: Message,
    i18n: TranslatorRunner,
    state: FSMContext,
    redis_source: RedisScheduleSource,
) -> None:
    data = await state.get_data()
    if data.get("periodic_tasks") is None:
        await message.answer(text=i18n.no.periodic.tasks())
    else:
        for task_id in data.get("periodic_tasks"):
            await redis_source.delete_schedule(task_id)
        await message.answer(text=i18n.periodic.tasks.deleted())


@commands_router.message(
    ~DialogStateGroupFilter(state_group=SettingsSG), Command("lang")
)
async def process_lang_command_sg(
    message: Message, dialog_manager: DialogManager, i18n: TranslatorRunner
) -> None:
    await dialog_manager.start(state=SettingsSG.lang)


@commands_router.message(
    DialogStateGroupFilter(state_group=SettingsSG),
    ~DialogStateFilter(state=SettingsSG.lang),
    Command("lang"),
)
async def process_lang_command(
    message: Message, dialog_manager: DialogManager, i18n: TranslatorRunner
) -> None:
    await dialog_manager.switch_to(state=SettingsSG.lang)


@commands_router.message(Command("help"))
async def process_help_command(
    message: Message, dialog_manager: DialogManager, i18n: TranslatorRunner
) -> None:
    await message.answer(text=i18n.help.command(), reply_markup=get_links_kb(i18n=i18n))
