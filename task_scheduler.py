import logging
from contextlib import suppress

from taskiq import TaskiqScheduler, TaskiqEvents, TaskiqState, Context, TaskiqDepends
from taskiq.schedule_sources import LabelScheduleSource
from taskiq_nats import NatsBroker


broker = NatsBroker("nats://localhost:4222", queue="notifying")
scheduler = TaskiqScheduler(broker, [LabelScheduleSource(broker)])


@broker.on_event(TaskiqEvents.WORKER_STARTUP)
async def startup(state: TaskiqState) -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)-8s [%(asctime)s] :: %(name)s : %(message)s"
    )
    logger = logging.getLogger(__name__)
    logger.warning("Starting scheduler...")

    state.logger = logger


@broker.on_event(TaskiqEvents.WORKER_SHUTDOWN)
async def shutdown(state: TaskiqState) -> None:
    state.logger.warning("Scheduler stopped")


@broker.task(task_name="notify", schedule=[{"cron": "* * * * *"}])
async def notify(context: Context = TaskiqDepends()) -> None:
    print("Оповещение!")