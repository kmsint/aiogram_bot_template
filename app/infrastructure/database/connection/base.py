from typing import Any
from app.infrastructure.database.query.results import MultipleQueryResults, SingleQueryResult


class BaseConnection:
    async def _fetch(
        self,
        sql: str,
        params: tuple[Any, ...] | list[tuple[Any, ...]] | None = None,
        connection: Any | None = None,
    ) -> MultipleQueryResults:
        raise NotImplementedError

    async def _fetchrow(
        self,
        sql: str,
        params: tuple[Any, ...] | list[tuple[Any, ...]] | None = None,
        connection: Any | None = None,
    ) -> SingleQueryResult:
        raise NotImplementedError

    async def _execute(
        self,
        sql: str,
        params: tuple[Any, ...] | list[tuple[Any, ...]] | None = None,
        connection: Any | None = None,
    ) -> None:
        raise NotImplementedError