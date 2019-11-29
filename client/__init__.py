import grpc
from protocol import test_pb2
from protocol import test_pb2_grpc
from server import filetree

def rebuildtree(namestr):
    new_tr = filetree.Tree()
    new_tr.deseriesFromPath(namestr)
    print(new_tr)

def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = test_pb2_grpc.testrpcStub(channel)

    print("-------------- TREE --------------")
    response = stub.getFiletree(test_pb2.TreeNameRequest())
    newtree = []
    for feature in response:
        newtree.append(feature.node_name)
    rebuildtree(newtree)

if __name__ == '__main__':
    run()