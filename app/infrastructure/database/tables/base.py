import logging
from typing import Any, Generic, TypeVar, Type, Dict, List, Optional
from app.database.connection.base import BaseConnection

T = TypeVar('T')

logger = logging.getLogger(__name__)


class BaseTable:
    __tablename__: str
    
    def __init__(self, connection: BaseConnection):
        self.connection = connection
    
    @property
    def tablename(self) -> str:
        return self.__tablename__
    
    def _sanitize_identifier(self, identifier: str) -> str:
        """Проверяет, что идентификатор содержит только допустимые символы."""
        import re
        if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', identifier):
            raise ValueError(f"Invalid SQL identifier: {identifier}")
        return identifier
