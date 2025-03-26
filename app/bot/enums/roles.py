from enum import Enum


class UserRole(str, Enum):
    ADMIN = "admin"
    OWNER = "owner"
    USER = "user"
