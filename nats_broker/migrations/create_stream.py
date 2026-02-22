import logging

import asyncio

from nats.aio.client import Client as NATS
from nats.js import JetStreamContext
from nats.js.api import RetentionPolicy, StorageType, StreamConfig

from app.config.loader import get_config

logger = logging.getLogger(__name__)


async def main():
    config = get_config()

    logging.basicConfig(
        level=logging._nameToLevel.get(
            config.logs.level_name.upper(),
            logging.INFO,
        ),
        format=config.logs.format,
    )

    nc = NATS()
    await nc.connect(servers=config.nats.servers)

    js: JetStreamContext = nc.jetstream()

    stream_name = config.nats.delayed_consumer_stream

    # Stream configuration
    stream_config = StreamConfig(
        name=stream_name,
        subjects=[config.nats.delayed_consumer_subject],
        retention=RetentionPolicy.LIMITS,
        storage=StorageType.FILE,
    )

    # Stream creation
    await js.add_stream(stream_config)

    logger.info("Stream `%s` created", stream_name)

    await nc.close()


asyncio.run(main())
