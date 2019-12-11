from utility import chunk
from masterlib import Register
import math

class AFile:
    def __init__(self):
        self.FileId = 0
        self.path = None # 文件路径
        self.size = 0 #文件大小
        self.ChunkList = [] # 主文件分块列表
        self.voter = [] # 第一阶段提交投票

    # 添加主文件分块
    def appendChunk(self, ch):
        if not isinstance(ch, chunk.chunk):
            return -1
        self.ChunkList.append(ch)
        return ch.ChunkId

    # 删除主文件分块
    def deleteChunk(self, CID):
        for item in self.ChunkList:
            if item.getChunkId() == CID:
                self.ChunkList.remove(item)
                return True
        return False

    def findbyoffset(self, offset):
        for item in self.ChunkList:
            if item.offset == offset:
                return item.getChunkId()
        return -1

    def setFszie(self,s):
        self.size = s

    def getFsize(self):
        return self.size

    def setFID(self,id):
        self.FileId = id

    def getFID(self):
        return self.FileId

    def setpath(self,path):
        self.path = path

    def getpath(self):
        return self.path

    def getChunk(self, cid):
        for item in self.ChunkList:
            if item.getChunkId() == cid:
                return item
        return None

    def getChunkList(self):
        return self.ChunkList

    def vote(self,cid):
        self.voter.append(cid)
        if len(self.voter) == len(self.ChunkList):
            return True
        else:
            return False

class FileManager:
    def __init__(self):
            self.FileSystem = {}
            self.FIDcout = 0
            self.CIDcout = 0
            self.Register = Register.Register() # dataserver 注册表

    # 创建新文件记录
    def CreateFile(self, path, size):
        newFile = AFile()
        newFile.setpath(path)
        self.FIDcout += 1
        newFile.setFID(self.FIDcout)
        newFile.setFszie(size)
        chunknumber = math.ceil(size/chunk.CHUNK_SIZE)
        for i in range(chunknumber):
            newChunk = chunk.chunk()
            self.CIDcout += 1
            newChunk.setCID(self.CIDcout)
            newChunk.setFileInfo(newFile.getFID(),i)
            newChunk.setDID(self.FindDataServer())
            self.upchunkonRegister(newChunk.getDataserverID(),1,newChunk)
            newFile.appendChunk(newChunk)
        self.FileSystem.setdefault(newFile.getFID(),newFile)
        self.show()
        return newFile

    def show(self):
        print('********************************************************************************************************')
        self.Register.show()
        print('-------------------------FileLogicManager Table-------------------------------------')
        print('   FileID  |         LogicPath        |    FileSize      |     ChunkList')
     #   print('------------------------------------------------------------------------------------')
        allchunk = []
        for key,item in self.FileSystem.items():
            listname = ''
            for achunk in item.getChunkList():
                listname += str(achunk.getChunkId()) + ','
                allchunk.append((achunk.getChunkId(),achunk.getFileID(),achunk.getOffset(),achunk.getDataserverID(),achunk.ChunkSize))
            print('No.%-10d %-30s %-12d %-s'%(key,item.getpath(),item.getFsize(),listname))
        print('------------------------ChunkManager Table----------------------------------------')
        print('   ChunkID  | from(FileID,offset)  |store(DataServerID)|    ChunkSize')
    #    print('---------------------------------------------------------------------------------')
        for record in allchunk:
            print('No.%-10d %5d %5d %20d %20d' % (record[0], record[1], record[2], record[3],record[4]))

    def vote(self,fid,cid):
        return self.FileSystem[fid].vote(cid)

    def readfile(self,path):
        Afile = self.FindByFilenama(path)
        chunklist = Afile.getChunkList()
        return chunklist
    def seekbyCID(self,cid):
        for key,afiles in self.FileSystem.items():
            for s in afiles.getChunkList():
                if s.getChunkId() == cid:
                    return key
        return 0

    def getNewCID(self):
        self.CIDcout += 1
        return self.CIDcout
    # 按ID查找
    def FindByFID(self,fid):
        return self.FileSystem.get(fid)
    # 按名查找
    def FindByFilenama(self, path):
        for files in self.FileSystem.values():
            if files.path == path:
                fids = files.FileId
                return self.FindByFID(fids)

    def deleteChunk(self,fid,cid):
        if not fid in self.FileSystem:
            return False
        return self.FileSystem[fid].deleteChunk(cid)
    # 删除文件记录
    def DeleteFile(self,fid):
        aFile = self.FileSystem.get(fid)
        for item in aFile.getChunkList():
            self.upchunkonRegister(item.getDataserverID(),-1,item)
        deleteRecord = self.FileSystem.pop(fid)
        self.show()
        return deleteRecord
    def FindByFileinfo(self,fid,offset):
        if not fid in self.FileSystem:
            return -1
        return self.FileSystem[fid].findbyoffset(offset)
    # 寻找文件块最少的服务器
    def FindDataServer(self):
        return self.Register.BestDataserver()
    #寻找排除掉主节点的文件块最少的服务器
    def FindBackupServer(self, did):
        return self.Register.BesetBackupserver(did)
    # 按照寻找
    def getChunk(self,fid,cid):
        if not fid in self.FileSystem:
            return None
        return self.FindByFID(fid).getChunk(cid)
    # 注册
    def RegistUp(self,ip,port):
        row = sys.Register.setrow(Register.HeadRegister().set(ip, port))
        self.show()
        return row
    # 查询
    def SeekSocket(self,did):
        ip = sys.Register.getrow(did).getIP()
        port = sys.Register.getrow(did).getport()
        return ip,port

    def SeekChunkOnDid(self,did):
        chunklist = self.Register.getrow(did).getchunklist()
        return chunklist

    def sizeOfonlineDataserver(self):
        return self.Register.getonlinedid()
    # 注销
    def LogOut(self,did):
        row = sys.Register.deleterow(did)
        self.show()
        return row

    def getalldataserver(self):
        return self.Register.getalldataserverdid()


    def upchunkonRegister(self,key,changeNum,achunk):
        self.Register.upchunkondataserver(key,changeNum,achunk)
        self.show()

    def uplive(self, key, newAlive):
        self.Register.uplive(key,newAlive)
        self.show()

    def upMainChunk(self,achunk):
        fid = achunk.getFileID()
        self.FileSystem[fid].appendChunk(achunk)
        self.show()

sys = FileManager()

if __name__ == '__main__':
    t0 = sys.RegistUp("1.2.3.4", 2000)
    t1 = sys.RegistUp("6.7.8.9", 3000)
    myfile = sys.CreateFile('c:/ss/l.dat',3674*1000)
    sys.DeleteFile(myfile.getFID())
    sys.LogOut(t1)
    sys.LogOut(t0)
    t3 = sys.RegistUp("5.7.8.9", 3000)

   # print(myfile.getFID())
    # print(myfile.getpath())
    # print(myfile.getFsize())
    # for chunk in myfile.ChunkList:
     #   print(chunk.getChunkId())
     #   print(chunk.getFileID())
     #   print(chunk.getOffset())
     #  print(chunk.getDataserverID())
     # print(sys.Register.getrow(chunk.getDataserverID()).IP)