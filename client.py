import grpc
import sys
from termcolor import colored
from protocol import test_pb2
from protocol import test_pb2_grpc
from utility import filetree


def rebuildtree(namestr):
    new_tr = filetree.Tree()
    new_tr.deseriesFromPath(namestr)
    return new_tr


def getTree():
    channel = grpc.insecure_channel('localhost:50051')
    stub = test_pb2_grpc.testrpcStub(channel)

    response = stub.getFiletree(test_pb2.TreeNameRequest())
    newtree = []
    for feature in response:
        newtree.append(feature.node_name)
    return rebuildtree(newtree)


def fetch():
    print('Fetching remote information.')
    try:
        file_tree = getTree()
        print("-------------- TREE --------------")
        print(file_tree)
    except:
        print(colored('Bad connection.', 'red'))
        print(colored('Please retry.', 'red'))

# 用户端命令行界面
def user_interface():
    fetch()
    while(True):
        print(colored("\nPlease input command:", 'green'), end='')
        cmd = input()
        if cmd.lower() == 'fetch':
            fetch()
        elif cmd.lower() == 'quit' or cmd == 'exit':
            exit(0)
        else:
            print('Invalid command. Please retry.')

if __name__ == '__main__':
    user_interface()
