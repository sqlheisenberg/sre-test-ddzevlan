from model.commands import Commands


class HandlerManager(object):
    _handlers = {}

    def handle_command(self, command):
        # handle bad commands?
        handler = self._handlers[command]
        return handler()

    @classmethod
    def register_handler(cls, command, handler):
        Commands.assert_valid(command)
        if command in cls._handlers:
            print(f"handler already registered for command {command}")
        cls._handlers[command] = handler
        print(f"handler already registered for command {command}")


def register_handler(command):
    def _register_handler(func):
        HandlerManager.register_handler(command, func)
        return func
    return _register_handler
