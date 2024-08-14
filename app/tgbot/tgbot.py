import asyncio
import logging

import asyncpg
import redis
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import ExceptionTypeFilter
from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram_dialog import setup_dialogs
from aiogram_dialog.api.exceptions import UnknownIntent, UnknownState
from fluentogram import TranslatorHub

from app.infrastructure.cache.utils.connect_to_redis import get_redis_pool
from app.infrastructure.database.utils.connect_to_pg import get_pg_pool
from app.infrastructure.storage.storage.nats_storage import NatsStorage
from app.infrastructure.storage.utils.nats_connect import connect_to_nats
from app.services.delay_service.utils.start_consumer import start_delayed_consumer
from app.tgbot.config.config import Config, load_config
from app.tgbot.dialogs.start.dialogs import start_dialog
from app.tgbot.handlers.commands import commands_router
from app.tgbot.handlers.errors import on_unknown_intent, on_unknown_state
from app.tgbot.middlewares.database import DataBaseMiddleware
from app.tgbot.middlewares.i18n import TranslatorRunnerMiddleware
from app.tgbot.middlewares.setlang import SetLangMiddleware
from app.tgbot.utils.i18n import create_translator_hub
from app.services.scheduler.task_scheduler import setup_taskiq, shutdown_taskiq

logger = logging.getLogger(__name__)


async def main():
    logger.info("Starting bot")

    config: Config = load_config()
    nc, js = await connect_to_nats(servers=config.nats.servers)

    storage: NatsStorage = await NatsStorage(
        nc=nc, 
        js=js, 
        key_builder=DefaultKeyBuilder(with_destiny=True)
    ).create_storage()

    bot = Bot(
        token=config.tg_bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher(storage=storage)

    logger.info(bot.__module__)
    logger.info(dp.__module__)

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

    translator_hub: TranslatorHub = create_translator_hub()

    logger.info("Registering error handlers")
    dp.errors.register(
        on_unknown_intent,
        ExceptionTypeFilter(UnknownIntent),
    )
    dp.errors.register(
        on_unknown_state,
        ExceptionTypeFilter(UnknownState),
    )

    dp.startup.register(setup_taskiq)
    dp.shutdown.register(shutdown_taskiq)

    logger.info("Including routers")
    dp.include_routers(commands_router, start_dialog)

    logger.info("Including middlewares")
    dp.update.middleware(DataBaseMiddleware())
    dp.update.middleware(SetLangMiddleware())
    dp.update.middleware(TranslatorRunnerMiddleware())
    dp.errors.middleware(DataBaseMiddleware())
    dp.errors.middleware(TranslatorRunnerMiddleware())
    dp.errors.middleware(SetLangMiddleware())

    setup_dialogs(dp)

    # Launch polling and delayed message consumer
    try:
        await asyncio.gather(
            dp.start_polling(
                bot, 
                js=js, 
                delay_del_subject=config.delayed_consumer.subject,
                _translator_hub=translator_hub,
                _db_pool=db_pool
            ), 
            start_delayed_consumer(
                nc=nc, 
                js=js, 
                bot=bot, 
                subject=config.delayed_consumer.subject,
                stream=config.delayed_consumer.stream,
                durable_name=config.delayed_consumer.durable_name
            )
        )
    except Exception as e:
        logger.exception(e)
    finally:
        await nc.close()
        logger.info('Connection to NATS closed')
        await db_pool.close()
        logger.info('Connection to Postgres closed')
        
