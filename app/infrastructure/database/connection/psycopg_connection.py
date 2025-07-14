from typing import Any

from psycopg import AsyncConnection
from psycopg.rows import dict_row

from app.infrastructure.database.connection.base import BaseConnection
from app.infrastructure.database.query.results import (
    MultipleQueryResult,
    SingleQueryResult,
)


class PsycopgConnection(BaseConnection):
    def __init__(self, connection: AsyncConnection) -> None:
        connection.row_factory = dict_row
        self._connection = connection

    async def execute(
        self,
        sql: str,
        params: tuple[Any, ...] | list[tuple[Any, ...]] | None = None,
        connection: Any | None = None,
    ) -> None:
        async with self._connection.cursor() as cur:
            await cur.execute(sql, params)

    async def fetchone(
        self,
        sql: str,
        params: tuple[Any, ...] | list[tuple[Any, ...]] | None = None,
        connection: Any | None = None,
    ) -> SingleQueryResult:
        async with self._connection.cursor() as cur:
            await cur.execute(sql, params)
            row = await cur.fetchone()
            return SingleQueryResult(row if row else None)

    async def fetchmany(
        self,
        sql: str,
        params: tuple[Any, ...] | list[tuple[Any, ...]] | None = None,
        connection: Any | None = None,
    ) -> MultipleQueryResult:
        async with self._connection.cursor() as cur:
            await cur.execute(sql, params)
            rows = await cur.fetchall()
            return MultipleQueryResult(rows)

    async def insert_and_fetchone(
        self,
        sql: str,
        params: tuple[Any, ...],
        connection: Any | None = None,
    ) -> SingleQueryResult:
        async with self._connection.cursor() as cur:
            await cur.execute(sql, params)
            row = await cur.fetchone()
            return SingleQueryResult(row if row else None)

    async def insert_and_fetchmany(
        self,
        sql: str,
        params: list[tuple[Any, ...]],
        connection: Any | None = None,
    ) -> MultipleQueryResult:
        async with self._connection.cursor() as cur:
            await cur.executemany(sql, params)
            rows = await cur.fetchall()
            return MultipleQueryResult(rows)

    async def update_and_fetchone(
        self,
        sql: str,
        params: tuple[Any, ...],
        connection: Any | None = None,
    ) -> SingleQueryResult:
        async with self._connection.cursor() as cur:
            await cur.execute(sql, params)
            row = await cur.fetchone()
            return SingleQueryResult(row if row else None)

    async def update_and_fetchmany(
        self,
        sql: str,
        params: list[tuple[Any, ...]],
        connection: Any | None = None,
    ) -> MultipleQueryResult:
        async with self._connection.cursor() as cur:
            await cur.executemany(sql, params)
            rows = await cur.fetchall()
            return MultipleQueryResult(rows)
