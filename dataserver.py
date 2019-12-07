import grpc
from protocol import MasterForData_pb2
from protocol import MasterForData_pb2_grpc
from datalib import StoreManager


def register():
    channel = grpc.insecure_channel('localhost:50051')
    stub = MasterForData_pb2_grpc.MFDStub(channel)
    response = stub.RegisteServer(MasterForData_pb2.socket(ip = 'localhost',port = 50000))
    StoreManager.StoreManager.setDID(response.id)

def serve():
    register()

if __name__ == '__main__':
    serve()
    print(StoreManager.StoreManager.getDID())