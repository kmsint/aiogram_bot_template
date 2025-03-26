import time

from app.services.scheduler.taskiq_broker import broker


@broker.task
async def simple_task():
    print()
    print("Это простая задача без расписания")
    print()


@broker.task(task_name="periodic_task", schedule=[{"cron": "* * * * *"}])
async def periodic_task():
    print()
    print(
        f"{time.strftime('%H:%M:%S', time.localtime(time.time()))}: Это периодическая задача, выполняющаяся раз в минуту"
    )
    print()


@broker.task
async def dynamic_periodic_task():
    print()
    print(
        f"{time.strftime('%H:%M:%S', time.localtime(time.time()))}: Это динамически запланированная периодическая задача"
    )
    print()


@broker.task
async def scheduled_task():
    print()
    print(
        f"{time.strftime('%H:%M:%S', time.localtime(time.time()))}: Это запланированная разовая задача"
    )
    print()
