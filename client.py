import grpc
from termcolor import colored
from protocol import MasterForClient_pb2
from protocol import MasterForClient_pb2_grpc
from protocol import DataForClient_pb2
from protocol import DataForClient_pb2_grpc
from utility import filetree
from utility import chunk
import atexit
import multiprocessing
import threading


def SendChunkToDataserver(args):
    address, cchunk = args
    print(cchunk.ChunkId, address)

    channel = grpc.insecure_channel(address)
    stub = DataForClient_pb2_grpc.DFCStub(channel)
    metadata = DataForClient_pb2.MetaData(
        ChunkSize = cchunk.ChunkSize,
        ChunkId = cchunk.getChunkId(),
        inFID = cchunk.getFileID(),
        offset = cchunk.getOffset(),
        StoreDID = cchunk.getDataserverID()
    )
    request = DataForClient_pb2.uploadChunkRequest(metadata=metadata, chunk=cchunk.getContent())

    response = stub.uploadChunk(request)
    channel.close()
    return response.Msg

def upfile(stub):
    sourcepath = 'ppp'
    contentarray ,sizes= chunk.split(sourcepath)
    destination = 'root'
    response = stub.getChunkInfoAndAllocatedDataServer(MasterForClient_pb2.getChunkInfoAndAllocatedDataServerRequest(
    size = sizes,
    path = destination
    ))
    chunknum = 0
    address = []
    allchunk = []
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
        address.append(str(ip)+':'+str(port))
        allchunk.append(chunks)

    with multiprocessing.Pool(4) as p:
        results = p.map(SendChunkToDataserver, zip(address,allchunk))
    print('update ok')
    print(results)

def getTree(stub):
    response = stub.getFiletree(MasterForClient_pb2.EmptyArg())
    newtree = []
    print()
    for feature in response:
        newtree.append((feature.name, feature.isFolder))

    filetree.FileTree.deseriesFromPath(newtree)

def update(stub):
    print('update')
    """ try:
        upfile(stub)
    except:
        print(colored('Bad connection.', 'red'))
        print(colored('Please retry.', 'red')) """
    upfile(stub)

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
        cmd = input().lower().strip()
        if cmd == 'fetch':
            fetch(stub)
        if cmd == 'update':
            update(stub)
        if cmd == 'delete':
            deleteFile(stub)
        elif cmd == 'quit' or cmd == 'exit':
            exit(0)
        else:
            print('Invalid command. Please retry.')

def ConnectMaster():
    channel = grpc.insecure_channel('localhost:50051')
    stub = MasterForClient_pb2_grpc.MFCStub(channel)
    return stub

def deleteFile(stub):
    toDelete = input('the file to delete: ')
    pakage = MasterForClient_pb2.FilePath(
        path=toDelete
    )
    ack = stub.deleteFile(pakage)
    print(ack.msg)


def requestDownloadFromMaster(stub):
    toDownload = input('the file to download: ')
    package = MasterForClient_pb2.downloadRequestInfo(
        path=toDownload
    )
    targetInfo = stub.requestDownloadFromMaster(package)
    chunknum = 0
    chunksList = []
    for chk in targetInfo:
        if chk.status == -1:
            print('Houston We Have a Problem --\nNo Such File!')
            return []
        # mychunk = chunk.chunk()
        # mychunk.ChunkSize = chk.ChunkSize
        # mychunk.setCID(chk.ChunkId)
        # mychunk.ip = chk.ip
        # mychunk.port = chk.port
        # chunknum += 1
        chunksList.append(chk)
        # 没有做master发过来chunks的完整性校验
    return chunksList




def ConnectDataServer(socket):
    channel = grpc.insecure_channel(socket)
    stub = DataForClient_pb2_grpc.DFCStub(channel)
    return stub

def downloadChunk(stub, CID):
    package = DataForClient_pb2.downloadRequest(
        ChunkId=CID
    )
    chunkData = stub.downloadChunk(package)
    return chunkData


    


if __name__ == '__main__':
    user_interface()

