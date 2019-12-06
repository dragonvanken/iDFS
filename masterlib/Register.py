class HeadRegister:
    def __init__(self):
        self.DID = 0
        self.IP = '0.0.0.0'
        self.Port = 0
        self.alive = 1# 1:live 0:eaded -1:uncertin
        self.chunknumber = 0

    def set(self,IP,Port,DID = 0,num =0, alive = 1):
        self.DID = DID
        self.IP = IP
        self.Port = Port
        self.alive = alive
        self.chunknumber = num
        return self

class Register:
    def __init__(self):
        self.table = dict()
        self.DIDstuct = 0

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

    def upchunk(self,key,changeNum):
        if not key in self.table:
            return -1
        self.table[key].chunknumber += changeNum
        return 0

    def BestDataserver(self):
        minvalue = 9999
        mindid = 0
        for rows in self.table.values():
            if rows.chunknumber < minvalue & rows.alive == 1:
                mindid = rows.DID
        return mindid


if __name__ == '__main__':
    RegisteTable = Register()
    row0 = HeadRegister()
    row0.set("1.2.3.4", 2000)
    row1 = HeadRegister()
    row1.set("6.7.8.9", 3000)
    t0= RegisteTable.setrow(row0)
    t1= RegisteTable.setrow(row1)
    print (RegisteTable.BestDataserver())
