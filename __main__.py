import asyncio
import logging

from config.config import settings

from app.tgbot import main

logging.basicConfig(
    level=logging.getLevelName(settings.logs.level_name),
    format=settings.logs.format
)

asyncio.run(main())