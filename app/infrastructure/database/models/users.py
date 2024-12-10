from dataclasses import dataclass
from datetime import datetime

from app.infrastructure.database.models.base import BaseModel
from app.tgbot.enums.roles import UserRole


@dataclass
class UsersModel(BaseModel):
    id: int
    user_id: int
    created: datetime
    tz_region: str | None
    tz_offset: str | None
    longitude: float | None
    latitude: float | None
    language: str
    role: UserRole
    is_alive: bool
    is_blocked: bool

    def __post_init__(self):
        self.role = UserRole(self.role)
