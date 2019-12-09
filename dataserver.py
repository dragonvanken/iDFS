import grpc
import socket
import multiprocessing
from termcolor import colored
from concurrent import futures
from protocol import MasterForData_pb2
from protocol import MasterForData_pb2_grpc
from protocol import DataForMaster_pb2
from protocol import DataForMaster_pb2_grpc
from protocol import DataForClient_pb2
from protocol import DataForClient_pb2_grpc
from utility import chunk
from datalib import StoreManager


MASTER_ADDRESS = 'localhost:50051'


def getEthIp():
    """返回本机局域网IP地址(str)"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


def getOpenPort():
    """选取一个空闲的端口并返回端口号(int)"""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", 0))
    s.listen(1)
    port = s.getsockname()[1]
    s.close()
    return int(port)

class DFM(DataForMaster_pb2_grpc.DFMServicer):
    def deleteChunkOnDataServer(self, request, context):
        cid = request.CID
        response = DataForMaster_pb2.ACK1(feedback = StoreManager.StoreManager.aborted(cid))
        return response

    def copyChunkBetweenDataServer(self, request, context):
        cid = request.CID
        address = request.copyip + ':' + str(request.copyport)
        cchunk = StoreManager.StoreManager.get(cid)
        cchunk.setCID(request.copycid)
        channel = grpc.insecure_channel(address)
        stub = DataForClient_pb2_grpc.DFCStub(channel)
        metadata = DataForClient_pb2.MetaData(
            ChunkSize=cchunk.ChunkSize,
            ChunkId=cchunk.getChunkId(),
            inFID=cchunk.getFileID(),
            offset=cchunk.getOffset(),
            StoreDID=cchunk.getDataserverID()
        )
        package = DataForClient_pb2.copyChunkRequest(metadata=metadata, chunk=cchunk.getContent())
        answer = stub.copyChunk(package)
        channel.close()
        if answer.Msg == 'ok':
            response = DataForMaster_pb2.ACK1(feedback=True)
        else:
            response= DataForMaster_pb2.ACK1(feedback=False)
        return response


def vote(FID, CID, status):
    channel = grpc.insecure_channel(MASTER_ADDRESS)
    stub = MasterForData_pb2_grpc.MFDStub(channel)
    response = stub.Recommit(MasterForData_pb2.recommitRequest(
        FID=FID,
        CID=CID,
        status=status)
    )
    channel.close()
    if True:
        StoreManager.StoreManager.commit(CID)
        print('Commit!')

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
        StoreManager.StoreManager.store(cchunk)

        # 投票
        vote(cchunk.getFileID(),cchunk.getChunkId(),1)

        return DataForClient_pb2.uploadChunkResponse(
            Msg='Saved!'
        )

    def copyChunk(self, request, context):
        cchunk = chunk.chunk()
        metadata = request.metadata
        content = request.chunk
        cchunk.ChunkSize = metadata.ChunkSize
        cchunk.ChunkId = metadata.ChunkId
        cchunk.inFID = metadata.inFID
        cchunk.offset = metadata.offset
        cchunk.StoreDID = StoreManager.StoreManager.getDID()
        cchunk.Content = content
        StoreManager.StoreManager.store(cchunk,True)
        print(cchunk.ChunkId, 'Backup Done!')
        return DataForClient_pb2.copyChunkResponse(
            Msg='ok'
        )

    def downloadChunk(self, request, context):
        cid = request.ChunkId
        theChunk = StoreManager.StoreManager.get(cid)
        package = DataForClient_pb2.dataOfChunk(
            ChunkSize=theChunk.ChunkSize,
            ChunkId=theChunk.getChunkId(),
            inFID=theChunk.getFileID(),
            offset=theChunk.getOffset(),
            Content=theChunk.getContent()
        )
        return package

def register():
    channel = grpc.insecure_channel(MASTER_ADDRESS)
    stub = MasterForData_pb2_grpc.MFDStub(channel)
    ip = getEthIp()
    port = getOpenPort()
    response = stub.RegisteServer(MasterForData_pb2.socket(ip=ip, port=port))
    StoreManager.StoreManager.setDID(response.id)
    return ip, port


def serve():
    ip, port = register()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=200))
    DataForClient_pb2_grpc.add_DFCServicer_to_server(DFC(), server)
    DataForMaster_pb2_grpc.add_DFMServicer_to_server(DFM(),server)
    server.add_insecure_port('[::]:' + str(port))
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
