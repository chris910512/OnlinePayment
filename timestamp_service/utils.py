from thrift.protocol import TBinaryProtocol
from thrift.transport import TSocket, TTransport
from timestamp_service.thrift_files import TimestampService


def get_timestamp():
    transport = TSocket.TSocket('localhost', 10000)
    transport = TTransport.TBufferedTransport(transport)
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    client = TimestampService.Client(protocol)
    transport.open()

    timestamp = client.getCurrentTimestamp()

    transport.close()

    return timestamp
