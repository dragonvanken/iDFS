class HeadRegister:
    def __init__(self):
        self.DID = 0
        self.IP = '0.0.0.0'
        self.Port = 0
        self.alive = 1# 1:live 0:uncertin
        self.chunknumber = 0
        self.chunklist = []

    def set(self,IP,Port,DID = 0,num =0,alive = 1):
        self.DID = DID
        self.IP = IP
        self.Port = Port
        self.alive = alive
        self.chunknumber = num
        return self

    def getDID(self):
        return self.DID

    def getIP(self):
        return self.IP

    def getport(self):
        return self.Port

    def getload(self):
        return self.chunknumber

    def getchunklist(self):
        return self.chunklist

    def getstatus(self):
        return self.alive

    def setload(self,load):
        self.chunknumber = load

    def setstatus(self,status):
        self.alive = status

    def appendchunklist(self,achunk):
        self.chunklist.append(achunk)

    def deletechunklist(self,achunk):
        self.chunklist.remove(achunk)

class Register:
    def __init__(self):
        self.table = dict()
        self.DIDstuct = 0

    def show(self):
        print('--------------------------Register Table--------------------------------------------')
        print('DataServerID |      IP       |    Port   |    status    |   Load   |  LoadList')
     #   print('-----------------------------------------------------------------------------------')
        for did,items in self.table.items():
            sss = ''
            if items.getstatus() == 1:
                status = 'online'
            else:
                status = 'uncertain'
            for chunks in items.getchunklist():
                sss += str(chunks.getChunkId())+','
            print('No.%-10d %-20s %-10d %-15s %-8d %-s'%(did, items.getIP(),items.getport(),status,items.getload(),sss))

    def setrow(self,row):
        if not isinstance(row, HeadRegister):
            return -1
        elif row.DID in self.table:
            return -1
        elif row.DID == 0:
            self.DIDstuct += 1
            if self.DIDstuct in self.table:
                self.DIDstuct += 1
            row.DID = self.DIDstuct
        self.table.setdefault(row.DID, row)
        return row.DID

    def getrow(self,key):
        if not key in self.table:
            return -1
        return self.table.get(key)

    def deleterow(self,key):
        if not key in self.table:
            return -1
        del self.table[key]
        return 0

    def uplive(self,key,newAlive):
        if not key in self.table:
            return -1
        self.table[key].alive = newAlive
        return 0

    def upchunkondataserver(self,key,changeNum,achunk):
        if not key in self.table:
            return -1
        self.table[key].chunknumber += changeNum
        if changeNum > 0:
            self.table[key].appendchunklist(achunk)
        else:
            self.table[key].deletechunklist(achunk)
        return 0

    def BestDataserver(self):
        minvalue = 9999
        mindid = -1
        for rows in self.table.values():
            if not rows.alive == 1:
                continue
            if rows.chunknumber < minvalue:
                mindid = rows.DID
                minvalue = rows.chunknumber
        return mindid

    def BesetBackupserver(self,did):
        minvalue = 9999
        mindid = -1
        for rows in self.table.values():
            if not rows.alive == 1:
                continue
            if rows.DID == did:
                continue
            if rows.chunknumber < minvalue:
                mindid = rows.DID
                minvalue = rows.chunknumber
        return mindid

    def getonlinedid(self):
        count = 0
        for rows in self.table.values():
            if rows.alive == 1:
                count += 1
        return count

    def getalldataserverdid(self):
        return list(self.table.keys())

if __name__ == '__main__':
    RegisteTable = Register()
    row0 = HeadRegister()
    row0.set("1.2.3.4", 2000)
    row1 = HeadRegister()
    row1.set("6.7.8.9", 3000)
    t0= RegisteTable.setrow(row0)
    t1= RegisteTable.setrow(row1)
    t = RegisteTable.getalldataserverdid()
    print (t)
