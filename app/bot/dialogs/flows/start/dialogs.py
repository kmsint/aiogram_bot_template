from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Format

from app.bot.dialogs.flows.start.getters import get_hello
from app.bot.dialogs.flows.start.states import StartSG
from app.bot.dialogs.widgets.i18n import I18nFormat

start_dialog = Dialog(
    Window(
        Format("{hello}"),
        I18nFormat("bot-desription"),
        getter=get_hello,
        state=StartSG.start,
    ),
)
