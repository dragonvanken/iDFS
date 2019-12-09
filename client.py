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

def upfile(stub, sourcepath, destination):
    contentarray ,sizes= chunk.split(sourcepath)
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

def isUniquePath(destination):
    return filetree.FileTree.seek(destination) is None

def upload(stub):
    print('uploading')
    """ try:
        upfile(stub)
    except:
        print(colored('Bad connection.', 'red'))
        print(colored('Please retry.', 'red')) """
    path = 'ppp'
    destination = 'root/ppp'
    if not isUniquePath(destination):
        print(colored('Unavailable path, please retry.', 'red'))
    else:
        upfile(stub, path, destination)
        print(colored('Successfully upload file '+path+' to '+destination,'green'))
    fetch(stub)

def fetch(stub):
    print('Fetching remote information.')
    try:
        getTree(stub)
        print("-------------- TREE --------------")
        filetree.FileTree.print_tree()
    except:
        print(colored('Bad connection.', 'red'))
        print(colored('Please retry.', 'red'))

def showAllCommands():
    print('iDFS is a Distribution File System written by WanKeJia group for NUDT distribution system cource.\n')
    print('All commands:')
    print('\tfetch:')
    print('\t\t更新并显示文件目录结构')

    print('\tupload')
    print('\t\t上传文件')

    print('\tdelete')
    print('\t\t删除文件')

    print('\tquit or exit')
    print('\t\t退出系统')
# 用户端命令行界面
def user_interface():
    stub = ConnectMaster()
    fetch(stub)
    while(True):
        print(colored("\nPlease input command:", 'green'), end='')
        cmd = input().lower().strip()
        if cmd == 'h' or cmd == 'help':
            showAllCommands()
        elif cmd == 'fetch':
            fetch(stub)
        elif cmd == 'upload':
            upload(stub)
        elif cmd == 'delete':
            deleteFile(stub)
        elif cmd == 'download':
            downloadFile(stub)
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


def requestDownloadFromMaster(stub, toDownload):
    package = MasterForClient_pb2.downloadRequestInfo(
        path=toDownload
    )
    targetInfo = stub.requestDownloadFromMaster(package)
    return targetInfo

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


def downloadFile(stub):
    path = input('the file to download: ').strip('/ ')
    chunksList = requestDownloadFromMaster(stub, path)
    dataList = []
    for chk in chunksList:
        if chk.status == 0:
            print('Houston We Have a Problem --\nSomething Goes Wrong!')
            return 0
        ip = chk.ip
        port = chk.port
        cid = chk.ChunkId
        mystub = ConnectDataServer(ip + ':' + str(port))
        chunkData = downloadChunk(mystub, cid)
        dataList.append(chunkData)
    name = path.split('/')[-1]
    chunk.merge(dataList, name)
    print('%s Download Successful!!'% name)
    return 1
    
if __name__ == '__main__':
    user_interface()

