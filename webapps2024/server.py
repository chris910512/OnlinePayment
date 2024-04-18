# server.py
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer
from thrift.transport import TSocket, TTransport
from timestamp_service.thrift_files import TimestampService
from datetime import datetime


class TimestampServiceHandler(TimestampService.Iface):
    def getCurrentTimestamp(self):
        return datetime.now().isoformat()


def start_server():
    handler = TimestampServiceHandler()
    processor = TimestampService.Processor(handler)
    transport = TSocket.TServerSocket(port=10000)
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()

    server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)

    print("Starting Thrift server...")
    server.serve()
