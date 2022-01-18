from tornado import gen, iostream
from tornado.log import app_log
from tornado.tcpclient import TCPClient
from config.app_config import AppConfig
from model.commands import Commands


class BlockchainTCPClient(object):
    def __init__(self) -> None:
        self.stream = None
        self.client = None

    @gen.coroutine
    def start(self) -> None:
        wait_sec = 5
        self.client = TCPClient()
        self.stream = yield self.client.connect(AppConfig.hostname,
                                                AppConfig.port)
        while True:
            try:
                print('Client-connected')
                yield self.why()
                yield self.who()
                yield self.where()
                yield gen.sleep(wait_sec)
            except iostream.StreamClosedError:
                app_log.error("connect error and again")
                yield gen.sleep(wait_sec)
                wait_sec = (wait_sec if (wait_sec >= 60) else (wait_sec * 2))

    @gen.coroutine
    def _execute_cmd(self, cmd) -> str:
        command_payload = self._prepare_command(cmd)
        yield self.stream.write(command_payload)
        raw_data = yield self.stream.read_bytes(
            AppConfig.max_buffer_size_client,
            partial=True)
        txt_data = str(raw_data, 'ascii')
        app_log.info(txt_data)
        return txt_data

    @gen.coroutine
    def where(self) -> str:
        result = yield self._execute_cmd(Commands.WHERE)
        print(str(result))

    @gen.coroutine
    def why(self) -> str:
        result = yield self._execute_cmd(Commands.WHY)
        print(str(result))

    @gen.coroutine
    def who(self) -> str:
        result = yield self._execute_cmd(Commands.WHO)
        print(str(result))

    def _prepare_command(self, cmd) -> str:
        padded = Commands.pad_to_command_len(cmd)
        return bytes(padded, 'ascii')
