import logging

from aiogram import Bot

from app.services.delay_service.consumer import DelayedMessageConsumer
from nats.aio.client import Client
from nats.js.client import JetStreamContext

logger = logging.getLogger(__name__)


async def start_delayed_consumer(
    nc: Client,
    js: JetStreamContext,
    bot: Bot,
    subject: str,
    stream: str,
    durable_name: str,
) -> None:
    consumer = DelayedMessageConsumer(
        nc=nc, js=js, bot=bot, subject=subject, stream=stream, durable_name=durable_name
    )
    logger.info("Start delayed message consumer")
    await consumer.start()
