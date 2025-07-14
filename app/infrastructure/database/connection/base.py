from abc import ABC, abstractmethod
from typing import Any

from app.infrastructure.database.query.results import (
    SingleQueryResult,
    MultipleQueryResult,
)


class BaseConnection(ABC):
    """
    Abstract base class for database connections.

    Provides a unified interface for executing SQL queries and fetching results.
    All interactions with the database driver should be implemented in subclasses.
    """

    @abstractmethod
    async def execute(
        self,
        sql: str,
        params: dict[str, Any] | None = None,
        connection: Any | None = None,
    ) -> None:
        """
        Execute a SQL command without returning any results (e.g., INSERT, UPDATE, DELETE).

        :param sql: SQL query string.
        :param params: Query parameters as a dict or list of dicts.
        :param connection: Optional active connection instance.
        """
        pass

    @abstractmethod
    async def fetchone(
        self,
        sql: str,
        params: dict[str, Any] | None = None,
        connection: Any | None = None,
    ) -> SingleQueryResult:
        """
        Execute a query and fetch a single result row.

        :param sql: SQL query string.
        :param params: Query parameters.
        :param connection: Optional active connection instance.
        :return: A single query result.
        :rtype: SingleQueryResult
        """
        pass

    @abstractmethod
    async def fetchmany(
        self,
        sql: str,
        params: dict[str, Any] | None = None,
        connection: Any | None = None,
    ) -> MultipleQueryResult:
        """
        Execute a query and fetch multiple result rows.

        :param sql: SQL query string.
        :param params: Query parameters.
        :param connection: Optional active connection instance.
        :return: Multiple query results.
        :rtype: MultipleQueryResult
        """
        pass

    @abstractmethod
    async def insert_and_fetchone(
        self,
        sql: str,
        params: dict[str, Any],
        connection: Any | None = None,
    ) -> SingleQueryResult:
        """
        Insert a single row and return the resulting data (e.g., using RETURNING *).

        :param sql: SQL INSERT statement with RETURNING clause.
        :param params: Query parameters as a tuple.
        :param connection: Optional active connection instance.
        :return: Inserted row.
        :rtype: SingleQueryResult
        """
        pass

    @abstractmethod
    async def insert_and_fetchmany(
        self,
        sql: str,
        params: list[dict[str, Any]],
        connection: Any | None = None,
    ) -> MultipleQueryResult:
        """
        Insert multiple rows and return the resulting data (e.g., using RETURNING *).

        :param sql: SQL INSERT statement with RETURNING clause.
        :param params: List of parameter tuples for batch insert.
        :param connection: Optional active connection instance.
        :return: Inserted rows.
        :rtype: MultipleQueryResult
        """
        pass

    @abstractmethod
    async def update_and_fetchone(
        self,
        sql: str,
        params: dict[str, Any],
        connection: Any | None = None,
    ) -> SingleQueryResult:
        """
        Update a row and return the resulting data.

        :param sql: SQL UPDATE statement with RETURNING clause.
        :param params: Query parameters.
        :param connection: Optional active connection instance.
        :return: Updated row.
        :rtype: SingleQueryResult
        """
        pass

    @abstractmethod
    async def update_and_fetchmany(
        self,
        sql: str,
        params: list[dict[str, Any]],
        connection: Any | None = None,
    ) -> MultipleQueryResult:
        """
        Update multiple rows and return the resulting data.

        :param sql: SQL UPDATE statement with RETURNING clause.
        :param params: List of parameter tuples for batch update.
        :param connection: Optional active connection instance.
        :return: Updated rows.
        :rtype: MultipleQueryResult
        """
        pass
