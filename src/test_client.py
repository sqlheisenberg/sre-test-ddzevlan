from tornado.ioloop import IOLoop
from tornado.log import app_log
from tornado import gen
from tornado.tcpclient import TCPClient
from config.app_config import AppConfig

stream = None
client = None


@gen.coroutine
def connect():
    global stream
    global client
    client = TCPClient()
    stream = yield client.connect(AppConfig.hostname, AppConfig.port)


@gen.coroutine
def send_command(cmd):
    try:

        yield stream.write(bytes(cmd, "ascii"))
        data = yield stream.read_bytes(
            AppConfig.max_buffer_size_client,
            partial=True
        )
        print(str(data, 'ascii'))
        return str(data, 'ascii')
    except Exception as err:
        app_log.error(f"{str(err)}")
    return None


@gen.coroutine
def client_main():
    yield connect()
    while True:
        yield send_command('WHYxx')
        yield send_command('WHERE')
        yield send_command('WHOxx')
        yield gen.sleep(5)


if __name__ == '__main__':
    client_main()
    IOLoop.current().start()
