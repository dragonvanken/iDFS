CHUNK_SIZE = 128 # HDFS-128MB
class chunk:
    def __init__(self):
        self.ChunkSize = CHUNK_SIZE # 文件块大小
        self.ChunkId = 0  # 块标记

        self.inFID = 0  # 属于哪一个文件
        self.offset = 0 # 文件块在文件内的偏移

        self.StoreDID = 0 # 存储服务器编号

        self.StoreAdress = None # 物理地址
        self.Context = None # 存储内容

        # read context from adress. Only can be used in DataServer
    def _loadContext(self):
        if self.StoreAdress is None:
            return -1
        self.Context = "need to write"

    def setCID(self,CID):
        self.ChunkId = CID

    def setDID(self,DID):
        self.StoreDID = DID

    def setFileInfo(self,fileid,offset):
        self.offset = offset
        self.inFID = fileid

    def setAdress(self, adress):
        self.StoreAdress = adress


    def getChunkId(self):
        return self.ChunkId

    def getDataserverID(self):
        return self.StoreDID

    def getOffset(self):
        return self.offset

    def getFileID(self):
        return self.inFID

    def getContext(self):
        self._loadContext()
        return self.Context