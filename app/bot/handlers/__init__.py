from .commands import commands_router

__all__ = ["routers"]

routers = [
    commands_router,
]
