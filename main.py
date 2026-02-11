import asyncio
import logging

from app.bot import main
from config.config import get_config

config = get_config()

logging.basicConfig(
    level=logging._nameToLevel.get(
        config.logs.level_name.upper(),
        logging.INFO,
    ),
    format=config.logs.format
)

asyncio.run(main())
