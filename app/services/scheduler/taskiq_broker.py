import logging

from taskiq import TaskiqEvents, TaskiqScheduler, TaskiqState
from taskiq.schedule_sources import LabelScheduleSource
from taskiq_nats import NatsBroker
from taskiq_redis import RedisScheduleSource

from config.config import settings

broker = NatsBroker(servers=settings.nats.servers, queue="taskiq_tasks")

redis_source = RedisScheduleSource(
    url=f"redis://{settings.redis.host}:{settings.redis.port}"
)

scheduler = TaskiqScheduler(broker, [redis_source, LabelScheduleSource(broker)])


@broker.on_event(TaskiqEvents.WORKER_STARTUP)
async def startup(state: TaskiqState) -> None:
    logging.basicConfig(level=settings.logs.level_name, format=settings.logs.format)
    logger = logging.getLogger(__name__)
    logger.info("Starting scheduler...")

    state.logger = logger


@broker.on_event(TaskiqEvents.WORKER_SHUTDOWN)
async def shutdown(state: TaskiqState) -> None:
    state.logger.info("Scheduler stopped")
