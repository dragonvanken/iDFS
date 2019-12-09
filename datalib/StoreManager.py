from utility import chunk
import  os
class StoreManage:
    def __init__(self):
        self.TmpChunk = {} #  临时存储表
        self.UsedChunk = {} # 永久存储表
        self.DID = 0

    def _EnAddress(self,cid):
        return str(cid)

    def store(self,achunk,used = False):
        if not isinstance(achunk,chunk.chunk):
            return False
        storeAddress = self._EnAddress(achunk.getChunkId())
        achunk.setAdress(storeAddress)
        chunk.savechunk(storeAddress,achunk)
        achunk.setContent(None)
        if used:
            self.UsedChunk.setdefault(achunk.getChunkId(),achunk)
        else :
            self.TmpChunk.setdefault(achunk.getChunkId(),achunk)
            self.show()
        return True

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
        self.show()
        return True

    def aborted(self, cid, used = True):
        if used:
            if not cid in self.UsedChunk:
                return False
            else:
                aachunk = self.UsedChunk.pop(cid)
                chunk.removechunk(aachunk)
                self.show()
                return True
        else:
            if not cid in self.TmpChunk:
                return False
            else:
                aachunk = self.TmpChunk.pop(cid)
                chunk.removechunk(aachunk)
                self.show()
                return True

    def setDID(self,did):
        self.DID = did
        self.show()
        return True

    def getDID(self):
        return  self.DID

    def show(self):
        print('***************************************************************************************************')
        print('The ServerID:',self.getDID())
        print('------------------------ChunkManager Table----------------------------------------')
        print('   ChunkID  | from(FileID,offset)  |store(Address)|   ChunkSize | status')
        for key,achunk in self.UsedChunk.items():
            print('No.%-10d %5d %5d %20d %15d %20s' % (key, achunk.getFileID(),achunk.getOffset(),achunk.getDataserverID(),achunk.ChunkSize,'Permanent Storage'))
        for key,achunk in self.TmpChunk.items():
            print('No.%-10d %5d %5d %20d %15d %20s' % (key, achunk.getFileID(),achunk.getOffset(),achunk.getDataserverID(),achunk.ChunkSize,'Temporary Storage'))

StoreManager = StoreManage()

if __name__ == '__main__':
    StoreManager.setDID(987)
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



