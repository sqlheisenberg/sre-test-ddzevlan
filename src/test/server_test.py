from contextlib import closing
import getpass
import os
import socket
import unittest

from config.app_config import AppConfig

from tornado.concurrent import Future
from tornado.netutil import bind_sockets, Resolver
from tornado.queues import Queue
from tornado.tcpclient import TCPClient, _Connector
from tornado.tcpserver import TCPServer
from tornado.testing import AsyncTestCase, gen_test
from tornado.test.util import skipIfNoIPv6, refusing_port, skipIfNonUnix
from tornado.gen import TimeoutError
from server import tcp_server
import typing

if typing.TYPE_CHECKING:
    from tornado.iostream import IOStream  # noqa: F401
    from typing import List, Dict, Tuple  # noqa: F401

# Fake address families for testing.  Used in place of AF_INET
# and AF_INET6 because some installations do not have AF_INET6.
AF1, AF2 = 1, 2

from handlers.handler_manager import HandlerManager

class TCPClientTest(AsyncTestCase):
    def setUp(self):
        super().setUp()
        self.server = None
        self.client = TCPClient()
        self.start_server()

    def start_server(self):
        self.server = tcp_server.TCPServer(HandlerManager())
        self.server.listen(AppConfig.port, AppConfig.hostname)

    def stop_server(self):
        if self.server is not None:
            self.server.stop()
            self.server = None

    def tearDown(self):
        self.client.close()
        self.stop_server()
        super().tearDown()

    @gen_test
    def test_connect(self):
        stream = yield self.client.connect(
            host=AppConfig.hostname, port=AppConfig.port
        )
        assert stream is not None
        