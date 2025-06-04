from psycopg import AsyncConnection

from app.infrastructure.database.connection.base import BaseConnection
from app.infrastructure.database.query.results import (
    MultipleQueryResult,
    SingleQueryResult,
)


class PsycopgConnection(BaseConnection):
    def __init__(self, connection: AsyncConnection) -> None:
        self._connection = connection

    async def execute(self, sql: str, params=None, connection=None):
        async with self._connection.cursor() as cur:
            await cur.execute(sql, params)

    async def fetchone(self, sql: str, params=None, connection=None) -> SingleQueryResult:
        async with self._connection.cursor() as cur:
            await cur.execute(sql, params)
            row = await cur.fetchone()
            return SingleQueryResult(dict(row) if row else None)

    async def fetchmany(self, sql: str, params=None, connection=None) -> MultipleQueryResult:
        async with self._connection.cursor() as cur:
            await cur.execute(sql, params)
            rows = await cur.fetchall()
            return MultipleQueryResult([dict(row) for row in rows])