from model.commands import Commands
from handlers.handler_manager import register_handler
from context.app_state import AppState


@register_handler(Commands.WHERE)
def where_handler():
    return str(AppState._instance.server_uuid)
