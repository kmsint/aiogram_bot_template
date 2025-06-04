import logging
from typing import Any
from app.infrastructure.database.connection.base import BaseConnection
from app.infrastructure.database.tables.enums.base import BaseTableActionEnum

logger = logging.getLogger(__name__)


class BaseTable:
    __tablename__: str

    def __init__(self, connection: BaseConnection):
        self.connection = connection

    def _log(self, action: str | BaseTableActionEnum, **kwargs: Any):
        logger.info(
            "Table='%s', Action='%s', Details: %s",
            self.__tablename__,
            action,
            ", ".join(f"{k}={v}" for k, v in kwargs.items()),
        )

    @property
    def tablename(self) -> str:
        return self.__tablename__
