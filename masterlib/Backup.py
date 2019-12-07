from utility import chunk
import random
class BackupQue:
    def __init__(self):
        self.backupList = []

    def append(self,achunk):
        if not isinstance(achunk , chunk.chunk):
            return False
        self.backupList.append(achunk)

    def delete(self,cid):
        for achunk in self.backupList:
            if achunk.getChunkId() == cid:
                self.backupList.remove(achunk)
                break

    def pop(self):
        return self.backupList.pop()

    def get(self):
        length = len(self.backupList)
        if not length > 0:
            return None
        random.seed()
        t = random.randint(0,length-1)
        return self.backupList[t]

    def getall(self):
        return self.backupList

class BackupManage:
    def __init__(self):
        self.MainAndBackupList = {} # 主键是主文件块cid，键值是备份文件块队列

    # 创建主文件块
    def CreateMainchunk(self,cid):
        if cid in self.MainAndBackupList:
            return False
        self.MainAndBackupList.setdefault(cid, BackupQue())
    # 替换主文件块，从备份中选取一个替代主文件块并返回，如果无备份则删除此条信息
    def UpdateMainchunk(self,maincid):
        if not maincid in self.MainAndBackupList:
            return None
        if self.MainAndBackupList[maincid] == BackupQue():
            self.MainAndBackupList.pop(maincid)
            return None
        newmainchunk = self.GetAbackup(maincid)
        self.DeleteAbackup(maincid, newmainchunk.getChunkId())
        bq = self.GetAbackupQue(maincid)

        self.CreateMainchunk(newmainchunk.getChunkId())
        self.CreateBackupQue(newmainchunk.getChunkId(),bq)

        self.MainAndBackupList.pop(maincid)
        return newmainchunk
    # 导入备份队列
    def CreateBackupQue(self, maincid, bq):
        if not maincid in self.MainAndBackupList:
            return False
        if not isinstance(bq, BackupQue):
            return False
        self.MainAndBackupList[maincid] = bq
        return True
    # 获取备份队列
    def GetAbackupQue(self, maincid):
        if not maincid in self.MainAndBackupList:
            return None
        return self.MainAndBackupList.get(maincid)
    # 删除备份列表
    def DeleteAbackupQue(self,maincid):
        if not maincid in self.MainAndBackupList:
            return None
        self.MainAndBackupList[maincid] = BackupQue()
    # 创建一个备份文件
    def CreateAbackup(self,maincid,achunk):
        if not maincid in self.MainAndBackupList:
            return False
        self.MainAndBackupList[maincid].append(achunk)
        return True
    # 随机获取一个备份文件
    def GetAbackup(self,maincid):
        if not maincid in self.MainAndBackupList:
            return None
        return self.MainAndBackupList.get(maincid).get()
    # 删除一个备份
    def DeleteAbackup(self,maincid,cid):
        if not maincid in self.MainAndBackupList:
            return False
        self.MainAndBackupList[maincid].delete(cid)
        return True

BackupManager = BackupManage()

if __name__ == '__main__':
    ac = chunk.chunk()
    ac.setCID(666)
    bc = chunk.chunk()
    bc.setCID(444)
    BackupManager.CreateMainchunk(9)
    BackupManager.CreateAbackup(9,ac)
    BackupManager.CreateAbackup(9, bc)
    newmainchunk = BackupManager.UpdateMainchunk(9)
    print(BackupManager.GetAbackup(newmainchunk.getChunkId()).getChunkId())