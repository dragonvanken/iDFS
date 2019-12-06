from utility import chunk
from masterlib import Register
import math

class AFile:
    def __init__(self):
        self.FileId = 0
        self.path = None # 文件路径
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

    def CreateFile(self, path, size):
        newFile = AFile()
        newFile.setpath(path)
        self.FIDcout += 1
        newFile.setFID(self.FIDcout)
        chunknumber = math.ceil(size/chunk.CHUNK_SIZE)
        for i in range(chunknumber):
            newChunk = chunk.chunk()
            self.CIDcout += 1
            newChunk.setCID(self.CIDcout)
            newChunk.setFileInfo(newFile.getFID(),i)
            newChunk.setDID(self.FindDataServer())

    # 寻找文件块最少的服务器
    def FindDataServer(self):
        return self.Register.BestDataserver()

sys = FileManager()

if __name__ == '__main__':
    sys.CreateFile('c:/ss/l.dat',1024)