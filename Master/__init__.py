from concurrent import futures
import time
import grpc
import MasterForClient_pb2
import MasterForClient_pb2_grpc
import filetree

class MFC(MasterForClient_pb2_grpc.MFCServicer):
    def __init__(self):
        a = filetree.AbstractNode('a')
        b = filetree.AbstractNode('b')
        c = filetree.AbstractNode('c')
        d = filetree.AbstractNode('d')
        e = filetree.AbstractNode('e')
        a.setbrother(b)
        b.addchild(c)
        c.setbrother(d)
        d.addchild(e)
        tr = filetree.Tree()
        tr.setroot(a)
        tr.makePath()
        self.db = tr.seriesToPath()
        print(self.db)

    def getFiletree(self, request, context):
        itemlist = []
        for item in self.db:
            respond = MasterForClient_pb2.Str(
                name = item)
            itemlist.append(respond)
        for answer in itemlist:
                yield answer

def serve()  :
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    MasterForClient_pb2_grpc.add_MFCServicer_to_server(MFC(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(60*60*24) # one day in seconds
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()