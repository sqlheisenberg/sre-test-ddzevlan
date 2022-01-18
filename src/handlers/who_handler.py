from model.commands import Commands
from handlers.handler_manager import register_handler
from context.app_state import AppState


@register_handler(Commands.WHO)
def who_handler():
    return str(AppState._instance.number_of_connected_clients)
