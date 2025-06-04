from app.infrastructure.database.tables.enums.base import BaseTableActionEnum


class UsersTableAction(BaseTableActionEnum):
    ADD = "add"
    DELETE = "delete"
    GET_USER = "get_user"
    UPDATE_ALIVE_STATUS = "update_alive_status"
    UPDATE_USER_LANG = "update_user_lang"
    UPDATE_BANNED_STATUS = "update_banned_status"
