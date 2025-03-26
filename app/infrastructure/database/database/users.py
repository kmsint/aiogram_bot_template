import logging
from datetime import datetime, timezone

from psycopg import AsyncConnection, AsyncCursor

from app.bot.enums.roles import UserRole
from app.infrastructure.database.models.users import UsersModel

logger = logging.getLogger(__name__)


class _UsersDB:
    __tablename__ = "users"

    def __init__(self, connection: AsyncConnection):
        self.connection = connection

    async def add(
        self,
        *,
        user_id: int,
        language: str,
        role: UserRole,
        is_alive: bool = True,
        is_blocked: bool = False,
    ) -> None:
        await self.connection.execute(
            """
            INSERT INTO users(user_id, language, role, is_alive, is_blocked)
            VALUES(%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING;
        """,
            (user_id, language, role.value, is_alive, is_blocked),
        )
        logger.info(
            "User added. db='%s', user_id=%d, date_time='%s', "
            "language='%s', role=%s, is_alive=%s, is_blocked=%s",
            self.__tablename__,
            user_id,
            datetime.now(timezone.utc),
            language,
            role.value,
            is_alive,
            is_blocked,
        )

    async def delete(self, *, user_id: int) -> None:
        await self.connection.execute(
            """
            DELETE FROM users WHERE user_id = %s;
        """,
            (user_id,),
        )
        logger.info("User deleted. db='%s', user_id='%d'", self.__tablename__, user_id)

    async def get_user_record(self, *, user_id: int) -> UsersModel | None:
        cursor: AsyncCursor = await self.connection.execute(
            """
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
            WHERE users.user_id = %s
        """,
            (user_id,),
        )
        data = await cursor.fetchone()
        return UsersModel(*data) if data else None

    async def update_alive_status(self, *, user_id: int, is_alive: bool = True) -> None:
        await self.connection.execute(
            """
            UPDATE users
            SET is_alive = %s
            WHERE user_id = %s
        """,
            (is_alive, user_id),
        )
        logger.info(
            "User updated. db='%s', user_id=%d, is_alive=%s",
            self.__tablename__,
            user_id,
            is_alive,
        )

    async def update_user_lang(self, *, user_id: int, user_lang: str) -> None:
        await self.connection.execute(
            """
            UPDATE users
            SET language = %s
            WHERE user_id = %s
        """,
            (user_lang, user_id),
        )
        logger.info(
            "User updated. db='%s', user_id=%d, language=%s",
            self.__tablename__,
            user_id,
            user_lang,
        )
