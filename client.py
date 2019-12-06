import grpc
from termcolor import colored
from protocol import MasterForClient_pb2
from protocol import MasterForClient_pb2_grpc
from utility import filetree
from utility import chunk
def SendChunkToDataserver(ip,port,chunks):
    print(chunks.getFileID())

def upfile(stub):
    sourcepath = 'ppp'
    contentarray ,sizes= chunk.split(sourcepath)
    destination = 'root'
    response = stub.getChunkInfoAndAllocatedDataServer(MasterForClient_pb2.getChunkInfoAndAllocatedDataServerRequest(
    size = sizes,
    path = destination
    ))
    chunknum = 0
    for feature in response:
        chunks = chunk.chunk()
        chunks.ChunkSize = feature.ChunkSize
        chunks.setCID(feature.ChunkId)
        chunks.setFileInfo(feature.inFID,feature.offset)
        chunks.setDID(feature.StoreDID)
        ip = feature.ip
        port = feature.port
        chunks.setContent(contentarray[chunknum])
        chunknum += 1
        SendChunkToDataserver(ip,port,chunks)
    print('update ok')

def getTree(stub):
    response = stub.getFiletree(MasterForClient_pb2.EmptyArg())
    newtree = []
    print()
    for feature in response:
        newtree.append((feature.name, feature.isFolder))

    filetree.FileTree.deseriesFromPath(newtree)

def update(stub):
    print('updata')
    try:
        upfile(stub)
    except:
        print(colored('Bad connection.', 'red'))
        print(colored('Please retry.', 'red'))

def fetch(stub):
    print('Fetching remote information.')
    try:
        getTree(stub)
        print("-------------- TREE --------------")
        filetree.FileTree.print_tree()
    except:
        print(colored('Bad connection.', 'red'))
        print(colored('Please retry.', 'red'))

# 用户端命令行界面
def user_interface():
    stub = ConnectMaster()
    fetch(stub)
    while(True):
        print(colored("\nPlease input command:", 'green'), end='')
        cmd = input()
        if cmd.lower() == 'fetch':
            fetch(stub)
        if cmd.lower() == 'update':
            update(stub)
        elif cmd.lower() == 'quit' or cmd == 'exit':
            exit(0)
        else:
            print('Invalid command. Please retry.')

def ConnectMaster():
    channel = grpc.insecure_channel('localhost:50051')
    stub = MasterForClient_pb2_grpc.MFCStub(channel)
    return stub

if __name__ == '__main__':
    user_interface()
