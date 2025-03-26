from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Format

from app.bot.dialogs.start.getters import get_hello
from app.bot.states.start import StartSG

start_dialog = Dialog(
    Window(Format("{hello}"), getter=get_hello, state=StartSG.start),
)
