import errno
import os
import socket
import ssl
from tornado import gen
from tornado.log import app_log
from tornado.ioloop import IOLoop
from tornado.iostream import IOStream, SSLIOStream
from tornado.netutil import bind_sockets, add_accept_handler, ssl_wrap_socket
from tornado import process
from tornado.util import errno_from_exception
import tornado.tcpserver
from handlers.handler_manager import HandlerManager
import typing
from typing import Union, Dict, Any, Iterable, Optional, Awaitable
from server import server_context_handler

if typing.TYPE_CHECKING:
    from typing import Callable, List  # noqa: F401

from model.commands import Commands


class TCPServer(tornado.tcpserver.TCPServer):

    def __init__(
        self,
        handler_manager: HandlerManager
    ) -> None:
        self._sockets = {}  # type: Dict[int, socket.socket]
        self._handlers = {}  # type: Dict[int, Callable[[], None]]
        self._pending_sockets = []  # type: List[socket.socket]
        self._started = False
        self._stopped = False
        self._handler_manager = handler_manager

    def listen(self, port: int, address: str = "") -> None:
        sockets = bind_sockets(port, address=address)
        self.add_sockets(sockets)

    def add_sockets(self, sockets: Iterable[socket.socket]) -> None:
        for sock in sockets:
            self._sockets[sock.fileno()] = sock
            self._handlers[sock.fileno()] = add_accept_handler(
                sock, self._handle_connection
            )

    def _handle_connection(self, connection: socket.socket,
                           address: Any) -> None:

        try:
            stream = IOStream(connection)
            future = self._handle_stream(stream, address)
            if future is not None:
                IOLoop.current().add_future(
                    gen.convert_yielded(future), lambda f: f.result()
                )
        except Exception:
            app_log.error("Error in connection callback", exc_info=True)

    async def _handle_stream(self, stream, address):
        server_context_handler.on_client_connected()
        while True:
            try:
                raw_data = await stream.read_bytes(Commands.get_command_len())
                command = self._try_parse_command(raw_data)
                response_data = self._handler_manager.handle_command(command)
                await stream.write(bytes(response_data, 'ascii'))
            except Exception as err:
                #app_log.error(f"{str(err)}")
                #app_log.error("Error in connection callback", exc_info=True)
                app_log.error("Error while handling client request/response")
                break
        server_context_handler.on_client_disconnected()

    def _try_parse_command(self, raw_data):
        raw_ascii = raw_data.decode('ascii')
        command = Commands.unpad_command(raw_ascii)
        Commands.assert_valid(command)
        return command
        