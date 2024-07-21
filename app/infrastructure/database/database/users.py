import logging
from datetime import datetime, timezone

from asyncpg import Connection

from app.infrastructure.database.models.users import UsersModel
from app.tgbot.enums.roles import UserRole

logger = logging.getLogger(__name__)


class _UsersDB:
    __tablename__ = 'users'

    def __init__(self, connection: Connection):
        self.connection = connection

    async def create_table(self) -> None:
        await self.connection.execute('''
            CREATE TABLE IF NOT EXISTS users(
                id SERIAL PRIMARY KEY,
                user_id BIGINT NOT NULL UNIQUE,
                created TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                tz_region VARCHAR(50),
                tz_offset VARCHAR(10),
                longitude REAL,
                latitude REAL,
                language VARCHAR(10),
                role VARCHAR(30),
                is_alive BOOLEAN NOT NULL,
                is_blocked BOOLEAN NOT NULL
            );
        ''')
        logger.info("Created table '%s'", self.__tablename__)

    async def add(
            self,
            *,
            user_id: int,
            language: str,
            role: UserRole,
            is_alive: bool = True,
            is_blocked: bool = False
    ) -> None:
        await self.connection.execute('''
            INSERT INTO users(user_id, language, role, is_alive, is_blocked)
            VALUES($1, $2, $3, $4, $5) ON CONFLICT DO NOTHING;
        ''', user_id, language, role.value, is_alive, is_blocked
        )
        logger.info(
            "User added. db='%s', user_id=%d, date_time='%s', "
            "language='%s', role=%s, is_alive=%s, is_blocked=%s",
            self.__tablename__, user_id, datetime.now(timezone.utc), language,
            role.value, is_alive, is_blocked
        )

    async def delete(self, *, user_id: int) -> None:
        await self.connection.execute('''
            DELETE FROM users WHERE user_id = $1;
        ''', user_id
        )
        logger.info(
            "User deleted. db='%s', user_id='%d'",
            self.__tablename__, user_id
        )

    async def get_user_record(self, *, user_id: int) -> UsersModel | None:
        cursor = await self.connection.cursor('''
            SELECT id,
                    user_id,
                    created,
                    tz_region,
                    tz_offset,
                    longitude,
                    latitude,
                    language,
                    role,
                    is_alive,
                    is_blocked
            FROM users
            WHERE users.user_id = $1
        ''', user_id
        )
        data = await cursor.fetchrow()
        return UsersModel(**data) if data else None

    async def update_alive_status(self, *, user_id: int, is_alive: bool = True) -> None:
        await self.connection.execute('''
            UPDATE users
            SET is_alive = $2
            WHERE user_id = $1
        ''', user_id, is_alive
        )
        logger.info(
            "User updated. db='%s', user_id=%d, is_alive=%s",
            self.__tablename__, user_id, is_alive
        )