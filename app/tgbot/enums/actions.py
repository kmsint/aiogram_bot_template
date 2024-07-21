from enum import Enum


class Action(str, Enum):
    DELETE = "delete"
    POST = "post"

print(Action.DELETE)