from tornado.ioloop import IOLoop
from server.tcp_server import TCPServer
from config.app_config import AppConfig
from handlers import *
from handlers.handler_manager import HandlerManager
from model.commands import Commands

manager = HandlerManager()
result = manager.handle_command(Commands.WHY)
print(f"Command result {result}")

result = manager.handle_command(Commands.WHO)
print(f"Command result {result}")

result = manager.handle_command(Commands.WHERE)
print(f"Command result {result}")

print(AppConfig.port)

server = TCPServer(manager)
server.listen(AppConfig.port, AppConfig.hostname)
IOLoop.current().start()
