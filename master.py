from concurrent import futures
import time
import grpc
from protocol import MasterForClient_pb2
from protocol import MasterForClient_pb2_grpc
from protocol import MasterForData_pb2
from protocol import MasterForData_pb2_grpc
from utility import filetree
from masterlib import Register

class MFC(MasterForClient_pb2_grpc.MFCServicer):
    def __init__(self):
        self.int = 1

    def getFiletree(self, request, context):
        itemlist = []
        for item in filetree.FileTree.seriesToPath():
            respond = MasterForClient_pb2.Str(
                name = item)
            itemlist.append(respond)
        for answer in itemlist:
                yield answer

def serve()  :
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    MasterForClient_pb2_grpc.add_MFCServicer_to_server(MFC(), server)
 #   MasterForData_pb2_grpc.add_MFDServicer_to_server()
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(60*60*24) # one day in seconds
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    filetree.FileTree.setroot(filetree.AbstractNode('root'))
    serve()

