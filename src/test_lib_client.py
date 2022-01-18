from tornado.ioloop import IOLoop
from client.blockchain_tcp_client import BlockchainTCPClient

client = BlockchainTCPClient()
client.start()
IOLoop.current().start()
