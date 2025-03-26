from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from app.bot.enums.actions import Action


@dataclass
class DelayedMessageDeletion:
    action_type: Action
    chat_id: int
    message_id: int
    sent_time: datetime
    delay: int

    def is_ready_time(self):
        return self.calc_delay() <= 0

    def calc_delay(self):
        return (
            self.sent_time + timedelta(seconds=self.delay) - datetime.now().astimezone()
        ).total_seconds()

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            action_type=Action(data.get("Tg-Delayed-Type")),
            chat_id=int(data.get("Tg-Delayed-Chat-ID")),
            message_id=int(data.get("Tg-Delayed-Msg-ID")),
            sent_time=datetime.fromtimestamp(
                float(data.get("Tg-Delayed-Msg-Timestamp")), tz=timezone.utc
            ),
            delay=int(data.get("Tg-Delayed-Msg-Delay")),
        )
