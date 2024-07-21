import asyncio
import nats
from nats.js.api import StreamConfig

async def main():
    # Подключение к NATS-серверу
    nc = await nats.connect("nats://localhost:4222")

    # Создание JetStream
    js = nc.jetstream()

    stream_name = "delayed_messages_aiogram"

    # Конфигурация стрима
    config = StreamConfig(
        name=stream_name,
        subjects=["aiogram.delayed.messages"],
        retention="limits",  # Политика хранения сообщений (limits, interest, workqueue)
        storage="file"  # Тип хранения сообщений (file, memory)
    )

    # Создание стрима
    await js.add_stream(config)

    print(f"Stream `{stream_name}` created")

    # Закрытие соединения
    await nc.close()


asyncio.run(main())
