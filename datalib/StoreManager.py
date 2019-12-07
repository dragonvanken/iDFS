from utility import chunk

class StoreManage:
    def __init__(self):
        self.TmpChunk = {} #  临时存储表
        self.UsedChunk = {} # 永久存储表
        self.DID = 0

    def _EnAddress(self,cid):
        return str(cid)

    def store(self,achunk,used = False):
        if not isinstance(achunk,chunk.chunk):
            return -1
        storeAddress = self._EnAddress(achunk.getChunkId())
        achunk.setAdress(storeAddress)
        chunk.savechunk(storeAddress,achunk)
        achunk.setContent(None)
        if used:
            self.UsedChunk.setdefault(achunk.getChunkId(),achunk)
        else :
            self.TmpChunk.setdefault(achunk.getChunkId(),achunk)

    def get(self,cid):
        if not cid in self.UsedChunk:
            return None
        address = self.UsedChunk.get(cid).getAddress()
        return chunk.readchunk(address)

    def commit(self,cid):
        if not cid in self.TmpChunk:
            return False
        achunk = self.TmpChunk.get(cid)
        self.UsedChunk.setdefault(cid,achunk)
        self.TmpChunk.pop(cid)

    def aborted(self, cid):
        if not cid in self.UsedChunk:
            return False
        else:
            self.UsedChunk.pop(cid)
            return True

    def setDID(self,did):
        self.DID = did

    def getDID(self):
        return  self.DID

StoreManager = StoreManage()

if __name__ == '__main__':
    achunk = chunk.chunk()
    achunk.setCID(7)
    achunk.setContent('are you OK?')
    StoreManager.store(achunk)
    StoreManager.commit(7)
    StoreManager.aborted(7)
    bchunk = StoreManager.get(7)
    if bchunk is not None:
        print(bchunk.getContent())
    else:
        print('NONE')



