import os
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
import time


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

    """ with multiprocessing.Pool(4) as p:
        results = p.map(SendChunkToDataserver, zip(address,allchunk)) """
    results = []
    for i in range(len(allchunk)):
        results.append(SendChunkToDataserver((address[i],allchunk[i])))
    print('upload ok')
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

def upload(stub, cur_node, user_input):
    try:
        path, destination = user_input.split()[1], user_input.split()[2]
        if not os.path.exists(path) or '/' in destination:
            raise Exception
    except:
        print(colored('Please specify valid file path and destination.', 'red'))
        return cur_node
    try:
        destination = cur_node.path + '/' + destination

        if not isUniquePath(destination):
            print(colored('Unavailable path, please retry.', 'red'))
        else:
            print('uploading.')
            upfile(stub, path, destination)
            print(colored('Successfully upload file '+path+' to '+destination,'green'))
            fetch(stub)
            cur_node = filetree.FileTree.seek(cur_node.path)
    except:
        print(colored('Bad connection.', 'red'))
        print(colored('Please retry.', 'red'))
        return cur_node
    return cur_node

def fetch(stub):
    print('Fetching remote information.')
    try:
        getTree(stub)
        print("-------------- TREE --------------")
        filetree.FileTree.print_tree()
    except:
        print(colored('Bad connection.', 'red'))
        print(colored('Please retry.', 'red'))

def showSubFiles(cur_node):
    nodes = cur_node.getChildren()
    if len(nodes) == 0:
        print('Empty folder.')
    else:
        for node in nodes:
            print(colored(node.name, 'green' if node.isFolder else None))

def cd(cur_node, user_input):
    destination = user_input.split()[1]
    if destination == '..':
        if cur_node.parent:
            cur_node = cur_node.parent
            print(cur_node.path)
    elif destination == '.':
        print(cur_node.path)
    else:
        target_path = cur_node.path + '/' + destination
        target_node = filetree.FileTree.seek(target_path)
        if target_node:
            if target_node.isFolder:
                cur_node = target_node
                print(cur_node.path)
            else:
                print(colored(destination+' is not a folder.', 'red'))
        else:
            print(colored(destination+' not found.', 'red'))
    return cur_node

def mkdir(stub, cur_node, user_input):
    dir_name = user_input.split()[1]
    destination = cur_node.path + '/' + dir_name
    if filetree.FileTree.seek(destination) is None:
        result = stub.createFolder(MasterForClient_pb2.createFolderRequest(destination=destination))
        if result.feedBack:
            print(colored('Create folder ' + dir_name + ' done.', 'green'))
            fetch(stub)
    else:
        print(colored(dir_name + ' is used, please chooes another folder name.', 'red'))

def showAllCommands():
    print('iDFS is a Distribution File System written by WanKeJia group for NUDT distribution system cource.\n')
    print('All commands:')

    print(colored('\tcd [folder]', 'green'))
    print('\t\t进入当前路径下的某个目录\n')

    print(colored('\tmkdir [folder]', 'green'))
    print('\t\t在当前路径下新建一个目录\n')

    print(colored('\tfetch','green'))
    print('\t\t更新并显示文件目录结构\n')

    print(colored('\tupload [file_path] [destination_path]', 'green'))
    print('\t\t上传本地文件到指定目录\n')

    print(colored('\tdelete', 'green'))
    print('\t\t删除文件\n')

    print(colored('\tquit/exit', 'green'))
    print('\t\t退出系统\n')

# 用户端命令行界面
def user_interface():
    stub = ConnectMaster()
    fetch(stub)
    cur_node = filetree.FileTree.root
    while(True):
        print(colored("\nPlease input command:", 'green'), end='')
        user_input = input().lower().strip()
        cmd = user_input.split()[0]

        if cmd == 'h' or cmd == 'help':
            showAllCommands()
        elif cmd == 'cd':
            cur_node = cd(cur_node, user_input)
        elif cmd == 'mkdir':
            mkdir(stub, cur_node, user_input)
        elif cmd == 'pwd':
            print(cur_node.path)
        elif cmd == 'ls':
            showSubFiles(cur_node)
        elif cmd == 'fetch':
            fetch(stub)
        elif cmd == 'upload':
            cur_node = upload(stub, cur_node, user_input)
        elif cmd == 'delete':
            cur_node = deleteFile(stub, cur_node, user_input)
        elif cmd == 'download':
            downloadFile(stub, cur_node, user_input)
        elif cmd == 'quit' or cmd == 'exit':
            exit(0)
        else:
            print('Invalid command. Please retry.')

def ConnectMaster():
    channel = grpc.insecure_channel('localhost:50051')
    stub = MasterForClient_pb2_grpc.MFCStub(channel)
    return stub

def deleteFile(stub, cur_node, user_input):
    try:
        toDelete = cur_node.path + '/' + user_input.split()[1]
    except:
        print(colored('Please specify file path'))
        return cur_node
    if filetree.FileTree.isUniquePath(toDelete):
        print(colored('No such file.', 'red'))
        return cur_node
    pakage = MasterForClient_pb2.FilePath(
        path=toDelete
    )
    ack = stub.deleteFile(pakage)
    print(ack.msg)
    fetch(stub)
    return filetree.FileTree.seek(cur_node.path)


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


def downloadFile(stub, cur_node, user_input):
    path = user_input.split()[1]
    path = cur_node.path + '/' + path
    if filetree.FileTree.isUniquePath(path):
        print(colored('No such file.', 'red'))
        return -1
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
        theChunk = chunk.chunk()
        theChunk.ChunkSize = chunkData.ChunkSize
        theChunk.ChunkId = chunkData.ChunkId
        theChunk.inFID = chunkData.inFID
        theChunk.offset = chunkData.offset
        theChunk.Content = chunkData.Content
        dataList.append(theChunk)
    name = path.split('/')[-1]
    chunk.merge(dataList, name)
    print('%s Download Successful!!'% name)
    return 1
    
if __name__ == '__main__':
    user_interface()

