import asyncio
import logging
import os
import sys

from app.bot import main
from config.config import settings

logging.basicConfig(
    level=logging.getLevelName(settings.logs.level_name), format=settings.logs.format
)

if sys.platform.startswith("win") or os.name == "nt":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

asyncio.run(main())
