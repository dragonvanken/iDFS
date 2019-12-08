from concurrent import futures
import time
import grpc
from protocol import MasterForClient_pb2
from protocol import MasterForClient_pb2_grpc
from protocol import MasterForData_pb2
from protocol import MasterForData_pb2_grpc
from protocol import DataForMaster_pb2
from protocol import DataForMaster_pb2_grpc
from utility import filetree
from masterlib import FileManager
from masterlib import Backup


class MFD(MasterForData_pb2_grpc.MFDServicer):
    def RegisteServer(self, request, context):
        ip = request.ip
        port = request.port
        print('regist!')
        return MasterForData_pb2.Num(
            id=FileManager.sys.RegistUp(ip, port))


class MFC(MasterForClient_pb2_grpc.MFCServicer):
    def getFiletree(self, request, context):
        itemlist = []
        for item in filetree.FileTree.seriesToPath():
            respond = MasterForClient_pb2.Str(
                name=item[0],
                isFolder=item[1])
            itemlist.append(respond)
        for answer in itemlist:
            yield answer

    def getChunkInfoAndAllocatedDataServer(self, request, context):
        size = request.size
        path = request.path

        # islegal(path) ? 目录树判断路径是否合法
        Files = FileManager.sys.CreateFile(path, size)
        respondlist = []

        for chunk in Files.ChunkList:
            respond = MasterForClient_pb2.ChunkStructor(
            ChunkSize = chunk.ChunkSize,
            ChunkId = chunk.getChunkId(),
            inFID = chunk.getFileID(),
            offset = chunk.getOffset(),
            StoreDID = chunk.getDataserverID(),
            ip = FileManager.sys.Register.getrow(chunk.getDataserverID()).getIP(),
            port = FileManager.sys.Register.getrow(chunk.getDataserverID()).getport()
            )
            respondlist.append(respond)
        for responds in respondlist:
            yield responds

    def deleteFile(self, request, context):
        FilePath = request.path
        # isFolder = request.isFolder
        msg0 = msg1 = 0
        listToDelete = []
        try:
            listToDelete = filetree.FileTree.getLeafNodes(FilePath)
        except:
            return MasterForClient_pb2.ACK(
                msg='Oops, no such directory or file',
                feedBack=False
            )

        msg0 = filetree.FileTree.removeNode(FilePath)
        if listToDelete:
            for fileName in listToDelete:
                msg2 = 0
                fileForFID = FileManager.sys.FindByFilenama(fileName)
                chunkList  = fileForFID.getChunkList()
                for chunk in chunkList:
                    did = chunk.getDataserverID()
                    cid = chunk.getChunkId()
                    response = deleteChunkOnDataServer(ConnectDataServer(did), cid)
                    if response.feedback:
                        msg2 += 1
                    Backup.BackupManager.insertDeleteTask(chunk.getFileID(),cid)
                if msg2 == len(chunkList):
                    msg1 += 1
                else: break
                FileManager.sys.DeleteFile(fileForFID.getFID())
        if msg0 and msg1 == len(listToDelete):
            return MasterForClient_pb2.ACK(
                msg='Successful!',
                feedBack=True
            )
        else:
            return MasterForClient_pb2.ACK(
                msg='Failed!',
                feedBack=False
            )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    MasterForClient_pb2_grpc.add_MFCServicer_to_server(MFC(), server)
    MasterForData_pb2_grpc.add_MFDServicer_to_server(MFD(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(60)  # one day in seconds 60*60*24
    except KeyboardInterrupt:
        server.stop(0)


def ConnectDataServer(DID):
    ip, port = FileManager.sys.SeekSocket(DID)
    channel = grpc.insecure_channel(ip + ':' + str(port))
    stub = DataForMaster_pb2_grpc.DFMStub(channel)
    return stub


def deleteChunkOnDataServer(stub, CID):
    # 删除成功返回 True， 否则 False
    pakage = DataForMaster_pb2.chunkID(
        CID=CID
    )
    return stub.deleteChunkOnDataServer(pakage)


if __name__ == '__main__':
    filetree.FileTree.setroot(filetree.AbstractNode('root', True))
    filetree.FileTree.insertNode('root/p', 1)
    filetree.FileTree.insertNode('root/qqq', 1)
    filetree.FileTree.insertNode('root/qqq/wanPijia1', 0)
    filetree.FileTree.insertNode('root/qqq/wanPijia2', 0)
    filetree.FileTree.insertNode('root/p/qwe', 0)
    newFile = FileManager.sys.CreateFile('root/p/qwe',1024 * 1000)
    FileManager.sys.FileSystem[newFile.getFID()].ChunkList[0].setCID(777)
    FileManager.sys.FileSystem[newFile.getFID()].ChunkList[0].setDID(1)
    serve()
