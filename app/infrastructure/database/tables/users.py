import logging
from datetime import datetime, timezone

from app.bot.enums.roles import UserRole
from app.infrastructure.database.connection.base import BaseConnection
from app.infrastructure.database.models.user import UserModel
from app.infrastructure.database.query.results import SingleQueryResult
from app.infrastructure.database.tables.base import BaseTable
from app.infrastructure.database.tables.enums.users import UsersTableAction

logger = logging.getLogger(__name__)


class UsersTable(BaseTable):
    __tablename__ = "users"

    def __init__(self, connection: BaseConnection):
        self.connection = connection

    async def add(
        self,
        *,
        user_id: int,
        language: str,
        role: UserRole,
        is_alive: bool = True,
        banned: bool = False,
    ) -> None:
        await self.connection.execute(
            sql="""
                INSERT INTO users(user_id, language, role, is_alive, banned)
                VALUES(%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING;
            """,
            params=(user_id, language, role, is_alive, banned),
        )
        self._log(
            UsersTableAction.ADD,
            user_id=user_id,
            created_at=datetime.now(timezone.utc),
            language=language,
            role=role,
            is_alive=is_alive,
            banned=banned,
        )

    async def delete(self, *, user_id: int) -> None:
        await self.connection.execute(
            sql="""
                DELETE FROM users WHERE user_id = %s;
            """,
            params=(user_id,),
        )
        self._log(UsersTableAction.DELETE, user_id=user_id)

    async def get_user(self, *, user_id: int) -> UserModel | None:
        data: SingleQueryResult = await self.connection.fetchone(
            sql="""
                SELECT id,
                    user_id,
                    created_at,
                    tz_region,
                    tz_offset,
                    longitude,
                    latitude,
                    language,
                    role,
                    is_alive,
                    banned
                FROM users
                WHERE users.user_id = %s
            """,
            params=(user_id,),
        )
        user_model: UserModel | None = data.to_model(model=UserModel)

        self._log(UsersTableAction.GET_USER, user_id=user_id)

        return user_model

    async def update_alive_status(self, *, user_id: int, is_alive: bool = True) -> None:
        await self.connection.execute(
            sql="""
                UPDATE users
                SET is_alive = %s
                WHERE user_id = %s
            """,
            params=(is_alive, user_id),
        )
        self._log(
            UsersTableAction.UPDATE_ALIVE_STATUS, user_id=user_id, is_alive=is_alive
        )

    async def update_user_lang(self, *, user_id: int, user_lang: str) -> None:
        await self.connection.execute(
            sql="""
                UPDATE users
                SET language = %s
                WHERE user_id = %s
            """,
            params=(user_lang, user_id),
        )
        self._log(
            UsersTableAction.UPDATE_USER_LANG, user_id=user_id, user_lang=user_lang
        )

    async def update_banned_status(self, *, user_id: int, banned: bool = False) -> None:
        await self.connection.execute(
            sql="""
                UPDATE users
                SET banned = %s
                WHERE user_id = %s
            """,
            params=(banned, user_id),
        )
        self._log(UsersTableAction.UPDATE_BANNED_STATUS, user_id=user_id, banned=banned)
