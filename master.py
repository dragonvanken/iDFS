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
from utility import chunk
from utility import network
from masterlib import FileManager
from masterlib import Backup


class MFD(MasterForData_pb2_grpc.MFDServicer):
    def RegisteServer(self, request, context):
        ip = request.ip
        port = request.port
        print('regist!')
        return MasterForData_pb2.Num(
            id=FileManager.sys.RegistUp(ip, port))

    def Recommit(self, request, context):
        iscommit = FileManager.sys.vote(request.FID, request.CID)

        if iscommit:
            # update filetree
            filetree.FileTree.insertNode(FileManager.sys.FindByFID(request.FID).path, False)
            # ask dataserver commit
            chunklist = FileManager.sys.FindByFID(request.FID).getChunkList()
            for c in chunklist:
                did = c.StoreDID
                cid = c.ChunkId
                ip, port = FileManager.sys.SeekSocket(did)
                channel = grpc.insecure_channel(ip+':'+str(port))
                stub = DataForMaster_pb2_grpc.DFMStub(channel)
                stub.recommitChunk(DataForMaster_pb2.chunkID(CID=cid))
                channel.close()
                # backup
                Backup.BackupManager.insertCreateTask(c.getFileID(), c.ChunkId)
        return MasterForData_pb2.recommitResponse(isCommit=iscommit)

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

    def createFolder(self, request, context):
        destination = request.destination
        return MasterForClient_pb2.ACK(feedBack=filetree.FileTree.insertNode(destination, True), msg='dummy message') 

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
        filetree.FileTree.print_tree()
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

    def requestDownloadFromMaster(self, request, context):
        requestFile = request.path
        temp = FileManager.sys.FindByFilenama(requestFile)
        if not temp:
            yield MasterForClient_pb2.targetInfo(
                status=0,
            )

        chunkList = temp.getChunkList()
        responseList = []
        for chk in chunkList:
            ip, port = FileManager.sys.SeekSocket(chk.getDataserverID())
            rsps = MasterForClient_pb2.targetInfo(
                ip = ip,
                port = port,
                ChunkSize = chk.ChunkSize,
                ChunkId = chk.ChunkId,
                status = 1
            )
            responseList.append(rsps)
        for response in responseList:
            yield response


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=200))
    MasterForClient_pb2_grpc.add_MFCServicer_to_server(MFC(), server)
    MasterForData_pb2_grpc.add_MFDServicer_to_server(MFD(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(5)  # one day in seconds 60*60*24
            heartbeat()  # 心跳检测
            startbackup() # 备份更新
    except KeyboardInterrupt:
        server.stop(0)

def heartbeat():
    examdid = FileManager.sys.getalldataserver()
    for did in list(examdid):
        try:
            # send heartpackage to DS
            stub = ConnectDataServer(did)
            response = sendheartbeat(stub,did)
            if response.feedback:
                if FileManager.sys.Register.getrow(did).getstatus() == 0:
                    FileManager.sys.uplive(did, 1)
                    newchunkondid = FileManager.sys.SeekChunkOnDid(did).copy()
                    if len(newchunkondid) > 0:
                        print('num:', len(newchunkondid))
                        for mainchunk in newchunkondid:
                            maincid = FileManager.sys.FindByFileinfo(mainchunk.getFileID(), mainchunk.getOffset())
                            if maincid >= 0:
                                Backup.BackupManager.createAbackup(maincid,mainchunk)
                            else:
                                did = mainchunk.getDataserverID()
                                cid = mainchunk.getChunkId()
                                response = deleteChunkOnDataServer(ConnectDataServer(did), cid)
                                FileManager.sys.upchunkonRegister(did,-1,mainchunk)

        except:
            if FileManager.sys.Register.getrow(did).getstatus() == 1:
                FileManager.sys.uplive(did,0)
                chunkondid = FileManager.sys.SeekChunkOnDid(did)
                if len(chunkondid) > 0:
                    for mainchunk in chunkondid:
                        ismain = FileManager.sys.deleteChunk(mainchunk.getFileID(), mainchunk.getChunkId())
                        if ismain:
                            newmainchunk = Backup.BackupManager.updateMainchunk(mainchunk.getChunkId())
                            if newmainchunk == None:
                                continue
                            FileManager.sys.upMainChunk(newmainchunk)
                            Backup.BackupManager.insertCreateTask(newmainchunk.getFileID(),newmainchunk.getChunkId())
                        else:
                            maincid= Backup.BackupManager.deleteBycid(mainchunk.getChunkId())
                            mainfid = FileManager.sys.seekbyCID(maincid)
                            Backup.BackupManager.insertCreateTask(mainfid,maincid)


def startbackup():
    while True:
        if not FileManager.sys.sizeOfonlineDataserver() > 1:
            print('The number of DataServer <= 1,The Backup sys close')
            break
        task = Backup.BackupManager.start()
        if task is None:
            break
        fid = task[0]
        cid = task[1]
        isCreatTask = task[2]
        if isCreatTask:
            achunk = FileManager.sys.getChunk(fid, cid)
            if achunk is None:
                continue
            did = achunk.getDataserverID()
            if Backup.BackupManager.isexist(cid,did):
                continue
            newchunk = chunk.chunk()
            newcid = FileManager.sys.getNewCID()
            newdid = FileManager.sys.FindBackupServer(achunk.getDataserverID())
            newchunk.setCID(newcid)
            newchunk.setDID(newdid)
            newchunk.setFileInfo(achunk.getFileID(),achunk.getOffset())
            newip, newport = FileManager.sys.SeekSocket(newdid)
            try:
                stub = ConnectDataServer(did)
                # send infomation to dataserver(ip,port) copy cid-chunk to newdataserver(newip,newport) as newcid-chunk
                copyChunkBetweenDataServer(stub,cid,newip,newport,newcid)
                FileManager.sys.upchunkonRegister(newdid,1,newchunk)
                Backup.BackupManager.end(cid,newchunk)
            except:
                print(str(cid)+'create backup failed!')
        else:
            bq = Backup.BackupManager.getAbackupQue(cid)
            if not bq is None:
                for achunk in bq.getall():
                    adid = achunk.getDataserverID()
                    try:
                        stub = ConnectDataServer(adid)
                        deleteChunkOnDataServer(stub,achunk.getChunkId())
                        FileManager.sys.upchunkonRegister(adid,-1,achunk)
                    except:
                        print(str(achunk.getChunkID()) + 'delete backup failed!')
            Backup.BackupManager.end(cid)

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

def copyChunkBetweenDataServer(stub,CID,copyip,copyport,copycid):
    package = DataForMaster_pb2.copyChunk(
        CID = CID,
        copyip= copyip,
        copyport=copyport,
        copycid= copycid
    )
    return stub.copyChunkBetweenDataServer(package)

def sendheartbeat(stub,did):
    package = DataForMaster_pb2.heartrequest(
        did =did
    )
    return stub.heartbeat(package)

if __name__ == '__main__':
    print("Master's IP is", network.getEthIp())
    filetree.FileTree.setroot(filetree.AbstractNode('root', True))
    FileManager.sys.show()
    serve()
