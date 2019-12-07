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
                break

    # 查找主文件分块
    def seekChunk(self, CID):
        for item in self.ChunkList:
            if item.getChunkId() == CID:
                return item

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
            self.Register.upchunknum(newChunk.getDataserverID(),1)
            newFile.appendChunk(newChunk)
        self.FileSystem.setdefault(newFile.getFID(),newFile)
        return newFile

    def getNewCID(self):
        self.CIDcout += 1
        return sys.CIDcout
    # 按ID查找AFile
    def FindByFID(self,fid):
        return self.FileSystem.get(fid)
    # 按名查找AFile
    def FindByFilenama(self, path):
        for files in self.FileSystem.values():
            if files.path == path:
                fids = files.FileId
                return self.FindByFID(fids)
    # 按ID查找DID
    def seekChunk(self,fid,cid):
        return self.FindByFID(fid).seekChunk(cid)
    # 删除文件记录
    def DeleteFile(self,fid):
        deleteRecord = self.FileSystem.pop(fid)
        return deleteRecord

    # 寻找文件块最少的服务器
    def FindDataServer(self):
        return self.Register.BestDataserver()
    # 注册
    def RegistUp(self,ip,port):
        return sys.Register.setrow(Register.HeadRegister().set(ip,port))
    # 查询
    def seekSocket(self,did):
        ip = sys.Register.getrow(did).getIP()
        port = sys.Register.getrow(did).getport()
        return ip,port
    # 注销
    def LogOut(self,did):
        return sys.Register.deleterow(did)

sys = FileManager()

if __name__ == '__main__':
    row0 = Register.HeadRegister()
    row0.set("1.2.3.4", 2000)
    row1 = Register.HeadRegister()
    row1.set("6.7.8.9", 3000)
    t0 = sys.Register.setrow(row0)
    t1 = sys.Register.setrow(row1)
    myfile = sys.CreateFile('c:/ss/l.dat',1024)
    t= sys.FindByFilenama('c:/ss/0l.dat')

   # print(myfile.getFID())
    # print(myfile.getpath())
    # print(myfile.getFsize())
    # for chunk in myfile.ChunkList:
     #   print(chunk.getChunkId())
     #   print(chunk.getFileID())
     #   print(chunk.getOffset())
     #  print(chunk.getDataserverID())
     # print(sys.Register.getrow(chunk.getDataserverID()).IP)