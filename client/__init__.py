import grpc
import MasterForClient_pb2
import MasterForClient_pb2_grpc
import filetree


def rebuildtree(namestr):
    new_tr = filetree.Tree()
    new_tr.deseriesFromPath(namestr)
    print(new_tr)

def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = MasterForClient_pb2_grpc.MFCStub(channel)

    print("-------------- TREE --------------")
    response = stub.getFiletree(MasterForClient_pb2.EmptyArg())
    newtree = []
    for feature in response:
        newtree.append(feature.name)
    rebuildtree(newtree)

if __name__ == '__main__':
    run()