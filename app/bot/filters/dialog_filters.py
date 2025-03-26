from aiogram.filters import BaseFilter
from aiogram.fsm.state import State, StatesGroup
from aiogram_dialog.api.protocols.manager import Context


class DialogStateFilter(BaseFilter):
    def __init__(self, state: State):
        self.state = state

    async def __call__(self, _, aiogd_context: Context | None, **kwargs) -> bool:
        if aiogd_context is None:
            return False
        else:
            return self.state == aiogd_context.state.state


class DialogStateGroupFilter(BaseFilter):
    def __init__(self, state_group: StatesGroup):
        self.state_group = state_group

    async def __call__(self, _, aiogd_context: Context | None, **kwargs) -> bool:
        if aiogd_context is None:
            return False
        else:
            return self.state_group == aiogd_context.state.group
