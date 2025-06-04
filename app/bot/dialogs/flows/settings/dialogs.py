from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button, Radio, Row, ScrollingGroup
from aiogram_dialog.widgets.text import Format

from app.bot.dialogs.flows.settings.getters import get_set_lang
from app.bot.dialogs.flows.settings.handlers import (
    cancel_set_lang,
    set_radio_lang_default,
    update_user_lang,
)
from app.bot.dialogs.flows.settings.states import SettingsSG

settings_dialog = Dialog(
    Window(
        Format("{set_lang}"),
        ScrollingGroup(
            Radio(
                checked_text=Format("🔘 {item[0]}"),
                unchecked_text=Format("⚪️ {item[0]}"),
                id="radio_lang",
                item_id_getter=lambda x: x[1],
                items="lang_buttons",
            ),
            id="lang_scroll",
            width=1,
            height=5,
            hide_on_single_page=True,
        ),
        Row(
            Button(
                text=Format("{back_button}"),
                id="set_lang_back_button_click",
                on_click=cancel_set_lang,
            ),
            Button(
                text=Format("{save_button}"),
                id="save_lang_button_click",
                on_click=update_user_lang,
            ),
        ),
        getter=get_set_lang,
        state=SettingsSG.lang,
    ),
    on_start=set_radio_lang_default,
)
