import logging

import asyncpg
import redis
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram_dialog import setup_dialogs
from fluentogram import TranslatorHub

from app.infrastructure.cache.utils.connect_to_redis import get_redis_pool
from app.infrastructure.database.utils.connect_to_pg import get_pg_pool
from app.infrastructure.database.utils.create_tables import create_tables
from app.infrastructure.storage.storage.nats_storage import NatsStorage
from aiogram.client.default import DefaultBotProperties
from app.infrastructure.storage.utils.connect_to_nats import get_nats_storage
from app.tgbot.config.config import Config, load_config
from app.tgbot.dialogs.start.dialogs import start_dialog
from app.tgbot.handlers.commands import commands_router
from app.tgbot.middlewares.database import DataBaseMiddleware
from app.tgbot.middlewares.i18n import TranslatorRunnerMiddleware
from app.tgbot.middlewares.setlang import SetLangMiddleware
from app.tgbot.utils.i18n import create_translator_hub

logger = logging.getLogger(__name__)


async def main():
    logger.info("Starting bot")

    config: Config = load_config()
    storage: NatsStorage = await get_nats_storage(
        servers=config.nats.servers, buckets=config.nats.buckets
    )

    bot = Bot(
        token=config.tg_bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher(storage=storage)

    if config.redis.use_cache:
        cache_pool: redis.asyncio.Redis = await get_redis_pool(
            db=config.redis.database,
            host=config.redis.host,
            port=config.redis.port,
            username=config.redis.username,
            password=config.redis.password,
        )
        dp.workflow_data.update(_cache_pool=cache_pool)

    db_pool: asyncpg.Pool = await get_pg_pool(
        db_name=config.pg.db_name,
        host=config.pg.host,
        port=config.pg.port,
        user=config.pg.username,
        password=config.pg.password,
    )

    async with db_pool.acquire() as connect:
        try:
            await create_tables(connect)
        except Exception as e:
            logger.exception(e)
            await db_pool.close()

    translator_hub: TranslatorHub = create_translator_hub()

    logger.info("Including routers")
    dp.include_routers(commands_router, start_dialog)

    logger.info("Including middlewares")
    dp.update.middleware(DataBaseMiddleware())
    dp.update.middleware(SetLangMiddleware())
    dp.update.middleware(TranslatorRunnerMiddleware())

    setup_dialogs(dp)

    await dp.start_polling(bot, _translator_hub=translator_hub, _db_pool=db_pool)
