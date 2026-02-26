import asyncio
import logging
from pathlib import Path

from app.bot import main as start_bot
from app.config.loader import get_config
from app.config.models import AppConfig


async def main() -> None:
    PROJECT_ROOT = Path(__file__).resolve().parent
    config: AppConfig = get_config()

    logging.basicConfig(
        level=config.logs.level_name.upper(),
        format=config.logs.format,
    )
    await start_bot(project_root=PROJECT_ROOT, config=config)


asyncio.run(main())
