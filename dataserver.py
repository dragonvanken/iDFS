import grpc
import socket
from concurrent import futures
from protocol import MasterForData_pb2
from protocol import MasterForData_pb2_grpc
from protocol import DataForMaster_pb2
from protocol import DataForMaster_pb2_grpc

from datalib import StoreManager
from protocol import DataForClient_pb2
from protocol import DataForClient_pb2_grpc
from utility import chunk
from datalib import StoreManager


class DFM(DataForMaster_pb2_grpc.DFMServicer):
    def deleteChunkOnDataServer(self, request, context):
        pass





def getEthIp():
    """返回本机局域网IP地址(str)"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

def getOpenPort():
    """选取一个空闲的端口并返回端口号(int)"""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("",0))
    s.listen(1)
    port = s.getsockname()[1]
    s.close()
    return int(port)

class DFC(DataForClient_pb2_grpc.DFCServicer):
    def uploadChunk(self, request, context):
        cchunk = chunk.chunk()
        metadata = request.metadata
        content = request.chunk
        cchunk.ChunkSize = metadata.ChunkSize
        cchunk.ChunkId = metadata.ChunkId
        cchunk.inFID = metadata.inFID
        cchunk.offset = metadata.offset
        cchunk.StoreDID = metadata.StoreDID
        cchunk.Content = content
        print(cchunk.ChunkId, 'Done!')
        return DataForClient_pb2.uploadChunkResponse(
            Msg = 'Good!'
        )

def register():
    channel = grpc.insecure_channel('localhost:50051')
    stub = MasterForData_pb2_grpc.MFDStub(channel)
    ip = getEthIp()
    port = getOpenPort()
    response = stub.RegisteServer(MasterForData_pb2.socket(ip = ip,port = port))
    StoreManager.StoreManager.setDID(response.id)
    return ip, port

def serve():
    ip, port = register()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=30))
    DataForClient_pb2_grpc.add_DFCServicer_to_server(DFC(), server)
    server.add_insecure_port('[::]:' + str(port))
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
    print(StoreManager.StoreManager.getDID())
