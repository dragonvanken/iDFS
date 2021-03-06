import pickle
import os
CHUNK_SIZE = 1000 * 1024 # 1MB
def merge(chunklist,address):
    sortsresult = {}
    bytesceam = bytes()
    for achunk in chunklist:
        sortsresult.setdefault(achunk.getOffset(),achunk.getContent())

    for i in range(0,len(sortsresult)):
            bytesceam += sortsresult.get(i)
    outputfile = open(address,'wb')
    outputfile.write(bytesceam)
    return True

def split(address):
    partnum = 0
    chunkarray = []
    inputfile = open(address, 'rb')  # open the fromfile
    sizes = os.path.getsize(address)
    while True:
        chunk = inputfile.read(CHUNK_SIZE)
        if not chunk:  # check the chunk is empty
            break
        partnum += 1
        chunkarray.append(chunk)
    return chunkarray,sizes

def savechunk(address,cchunk):
    with open(address, 'wb') as f:  # open file with write-mode
        picklestring = pickle.dump(cchunk, f)

def readchunk(address):
    with open(address, 'rb') as f:  # open file with write-mode
         return pickle.load(f)

def removechunk(achunk):
    path = achunk.getAddress()
    os.remove(path)

class chunk:
    def __init__(self):
        self.ChunkSize = CHUNK_SIZE # 文件块大小
        self.ChunkId = 0  # 块标记

        self.inFID = 0  # 属于哪一个文件
        self.offset = 0 # 文件块在文件内的偏移

        self.StoreDID = 0 # 存储服务器编号

        self.StoreAdress = None # 物理地址 only in DataServer
        self.Content = None # 存储内容

    def appendContent(self,content):
        self.Content += content

    def setCID(self,CID):
        self.ChunkId = CID

    def setDID(self,DID):
        self.StoreDID = DID

    def setFileInfo(self,fileid,offset):
        self.offset = offset
        self.inFID = fileid

    def setAdress(self, adress):
        self.StoreAdress = adress

    def setContent(self,content):
        self.Content = content

    def getChunkId(self):
        return self.ChunkId

    def getDataserverID(self):
        return self.StoreDID

    def getOffset(self):
        return self.offset

    def getFileID(self):
        return self.inFID

    def getAddress(self):
        return self.StoreAdress

    def getContent(self):
        return self.Content



