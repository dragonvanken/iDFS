import grpc
from termcolor import colored
from protocol import MasterForClient_pb2
from protocol import MasterForClient_pb2_grpc
from utility import filetree


def getTree():
    channel = grpc.insecure_channel('localhost:50051')
    stub = MasterForClient_pb2_grpc.MFCStub(channel)
    response = stub.getFiletree(MasterForClient_pb2.EmptyArg())
    newtree = []
    print()
    for feature in response:
        newtree.append(feature.name)

    filetree.FileTree.deseriesFromPath(newtree)


def fetch():
    print('Fetching remote information.')
    try:
        getTree()
        print("-------------- TREE --------------")
        print(filetree.FileTree)
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
