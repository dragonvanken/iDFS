import grpc
from concurrent import futures
from protocol import MasterForData_pb2
from protocol import MasterForData_pb2_grpc
from protocol import DataForClient_pb2
from protocol import DataForClient_pb2_grpc
from utility import chunk

DID = []

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
    response = stub.RegisteServer(MasterForData_pb2.socket(ip = 'localhost',port = 50000))
    DID.append(response.id)

def serve():
    register()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=30))
    DataForClient_pb2_grpc.add_DFCServicer_to_server(DFC(), server)
    server.add_insecure_port('[::]:50000')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
    print(DID)
