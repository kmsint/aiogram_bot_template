from datetime import datetime

from app.bot.enums.actions import Action
from nats.js.client import JetStreamContext


async def delay_message_deletion(
    js: JetStreamContext, chat_id: int, message_id: int, subject: str, delay: int = 0
) -> None:
    headers = {
        "Tg-Delayed-Type": Action.DELETE,
        "Tg-Delayed-Chat-ID": str(chat_id),
        "Tg-Delayed-Msg-ID": str(message_id),
        "Tg-Delayed-Msg-Timestamp": str(datetime.now().timestamp()),
        "Tg-Delayed-Msg-Delay": str(delay),
    }
    await js.publish(subject=subject, headers=headers)


async def delay_message_senging(
    js: JetStreamContext, chat_id: int, text: str, subject: str, delay: int = 0
) -> None:
    headers = {
        "Tg-Delayed-Type": Action.POST,
        "Tg-Delayed-Chat-ID": str(chat_id),
        "Tg-Delayed-Msg-Timestamp": str(datetime.now().timestamp()),
        "Tg-Delayed-Msg-Delay": str(delay),
    }
    payload = text.encode(encoding="utf-8")
    await js.publish(subject=subject, payload=payload, headers=headers)
