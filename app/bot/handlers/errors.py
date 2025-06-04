import logging

from aiogram_dialog import DialogManager, ShowMode, StartMode

from app.bot.dialogs.flows.start.states import StartSG

logger = logging.getLogger(__name__)


async def on_unknown_intent(event, dialog_manager: DialogManager):
    # Example of handling UnknownIntent Error and starting new dialog.
    logging.error("Restarting dialog: %s", event.exception)
    await dialog_manager.start(
        StartSG.start,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.SEND,
    )


async def on_unknown_state(event, dialog_manager: DialogManager):
    # Example of handling UnknownState Error and starting new dialog.
    logging.error("Restarting dialog: %s", event.exception)
    await dialog_manager.start(
        StartSG.start,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.SEND,
    )
