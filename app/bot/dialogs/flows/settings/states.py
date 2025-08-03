from aiogram.fsm.state import State, StatesGroup


class SettingsSG(StatesGroup):
    lang = State()
