from app.infrastructure.database.connection.base import BaseConnection
from app.infrastructure.database.tables.users import UsersTable


class DB:
    def __init__(self, connection: BaseConnection) -> None:
        self.users = UsersTable(connection=connection)
