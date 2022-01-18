from model.commands import Commands
from handlers.handler_manager import register_handler
from config.app_config import AppConfig


@register_handler(Commands.WHY)
def why_handler():
    return AppConfig.why_response
