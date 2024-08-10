import asyncio
import logging

import taskiq_aiogram
from aiogram import Bot
from taskiq import InMemoryBroker, TaskiqDepends

logger = logging.getLogger(__name__)

broker = InMemoryBroker()

# This line is going to initialize everything.
taskiq_aiogram.init(
    broker,
    # This is path to the dispatcher.
    "app.tgbot.tgbot.main:dp",
    # This is path to the bot instance.
    "app.tgbot.tgbot.main:bot",
    # You can specify more bots here.
)


@broker.task(task_name="my_task")
async def my_task(chat_id: int, bot: Bot = TaskiqDepends()) -> None:
    print("I'm a task")
    await asyncio.sleep(4)
    await bot.send_message(chat_id, "task completed")


# Taskiq calls this function when starting the worker.
async def setup_taskiq(bot: Bot, *_args, **_kwargs):
    # Here we check if it's a clien-side,
    # Because otherwise you're going to
    # create infinite loop of startup events.
    if not broker.is_worker_process:
        logging.info("Setting up taskiq")
        await broker.startup()


# Taskiq calls this function when shutting down the worker.
async def shutdown_taskiq(bot: Bot, *_args, **_kwargs):
    if not broker.is_worker_process:
        logging.info("Shutting down taskiq")
        await broker.shutdown()