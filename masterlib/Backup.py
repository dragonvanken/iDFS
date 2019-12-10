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

    def clear(self):
        self.backupList.clear()

    def isempty(self):
        if len(self.backupList) > 0:
            return False
        else:
            return True

class BackupManage:
    def __init__(self):
        self.MainAndBackupList = {} # 主键是主文件块cid，键值是备份文件块队列
        self.BackupTask = [] # 备份任务,(文件块cid,操作）true表示增加 false表示删除
    # 创建主文件块
    def createMainchunk(self,cid):
        if cid in self.MainAndBackupList:
            return False
        self.MainAndBackupList.setdefault(cid, BackupQue())
    # 替换主文件块，从备份中选取一个替代主文件块并返回，如果无备份则删除此条信息
    def updateMainchunk(self,maincid):
        if not maincid in self.MainAndBackupList:
            return None
        if self.MainAndBackupList[maincid].isempty():
            self.MainAndBackupList.pop(maincid)
            return None
        newmainchunk = self.getAbackup(maincid)
        self.deleteAbackup(maincid, newmainchunk.getChunkId())
        bq = self.getAbackupQue(maincid)

        self.createMainchunk(newmainchunk.getChunkId())
        self.createBackupQue(newmainchunk.getChunkId(),bq)

        self.MainAndBackupList.pop(maincid)
        return newmainchunk
    # 导入备份队列
    def createBackupQue(self, maincid, bq):
        if not maincid in self.MainAndBackupList:
            return False
        if not isinstance(bq, BackupQue):
            return False
        self.MainAndBackupList[maincid] = bq
        return True
    # 获取备份队列
    def getAbackupQue(self, maincid):
        if not maincid in self.MainAndBackupList:
            return None
        return self.MainAndBackupList.get(maincid)
    # 删除备份列表
    def deleteAbackupQue(self,maincid):
        if not maincid in self.MainAndBackupList:
            return None
        self.MainAndBackupList[maincid].clear()
    # 创建一个备份文件
    def createAbackup(self,maincid,achunk):
        if not maincid in self.MainAndBackupList:
            return False
        self.MainAndBackupList[maincid].append(achunk)
        return True
    # 随机获取一个备份文件
    def getAbackup(self,maincid):
        if not maincid in self.MainAndBackupList:
            return None
        return self.MainAndBackupList.get(maincid).get()
    # 删除一个备份
    def deleteAbackup(self,maincid,cid):
        if not maincid in self.MainAndBackupList:
            return False
        self.MainAndBackupList[maincid].delete(cid)
        return True
    # 添加需要备份的任务
    def insertCreateTask(self,fid,cid):
        self.BackupTask.append((fid,cid,True))
        print('create a backup:'+str(cid))
    # 添加需要删除备份的任务
    def insertDeleteTask(self,fid,cid):
        self.BackupTask.append((fid,cid,False))
        print('delete a backup:' + str(cid))
    # 开始一个备份任务
    def start(self):
        if not len(self.BackupTask) > 0:
            return None
        return self.BackupTask.pop(0)
    # 完成一个备份任务 任务以及任务结果
    def end(self,maincid,achunk = None):
        if achunk is None:
            self.deleteAbackupQue(maincid)
            self.updateMainchunk(maincid)
        else:
            if maincid not in self.MainAndBackupList:
                self.createMainchunk(maincid)
            self.createAbackup(maincid, achunk)


BackupManager = BackupManage()

if __name__ == '__main__':
    ac = chunk.chunk()
    ac.setCID(666)
    bc = chunk.chunk()
    bc.setCID(444)
    BackupManager.createMainchunk(9)
    BackupManager.createAbackup(9,ac)
    BackupManager.createAbackup(9, bc)
    newmainchunk = BackupManager.updateMainchunk(9)
    print(BackupManager.getAbackup(newmainchunk.getChunkId()).getChunkId())