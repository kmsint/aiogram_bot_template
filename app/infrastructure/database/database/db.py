from asyncpg import Connection

from app.infrastructure.database.database.users import _UsersDB


class DB:
    def __init__(self, connection: Connection) -> None:
        self.users = _UsersDB(connection=connection)