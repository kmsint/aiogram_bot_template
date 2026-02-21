import asyncio
import logging
from pathlib import Path

from app.bot import main as start_bot
from app.config.loader import get_config


async def main():
    PROJECT_ROOT = Path(__file__).resolve().parent
    config = get_config()

    logging.basicConfig(
        level=logging._nameToLevel.get(
            config.logs.level_name.upper(),
            logging.INFO,
        ),
        format=config.logs.format
    )
    await start_bot(project_root=PROJECT_ROOT, config=config)

asyncio.run(main())