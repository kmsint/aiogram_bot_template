from typing import Any
from app.infrastructure.database.query.results import (
    MultipleQueryResult,
    SingleQueryResult,
)


class BaseConnection:
    async def execute(
        self,
        sql: str,
        params: tuple[Any, ...] | list[tuple[Any, ...]] | None = None,
        connection: Any | None = None,
    ) -> None:
        raise NotImplementedError

    async def fetchmany(
        self,
        sql: str,
        params: tuple[Any, ...] | list[tuple[Any, ...]] | None = None,
        connection: Any | None = None,
    ) -> MultipleQueryResult:
        raise NotImplementedError

    async def fetchone(
        self,
        sql: str,
        params: tuple[Any, ...] | list[tuple[Any, ...]] | None = None,
        connection: Any | None = None,
    ) -> SingleQueryResult:
        raise NotImplementedError
