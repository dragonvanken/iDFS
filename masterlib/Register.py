class HeadRegister:
    def __init__(self):
        self.DID = 0
        self.IP = "0.0.0.0"
        self.Port = 0
        self.alive = 1# 1:live 0:eaded -1:uncertin
        self.chunknumber = 0

    def set(self,IP,Port,DID = 0,alive = 1,num =0):
        self.DID = DID
        self.IP = IP
        self.Port = Port
        self.alive = alive
        self.chunknumber = num

class Register:
    def __init__(self):
        self.table = dict()
        self.IDstuct = 0

    def set(self,row):
        if not isinstance(row, HeadRegister):
            return -1
        elif row.DID in self.table:
            return -1
        elif row.DID == 0:
            self.IDstuct += 1
            if self.IDstuct in self.table:
                self.IDstuct += 1
            row.DID = self.IDstuct
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


RegisteTable = Register()

if __name__ == '__main__':
    row0 = HeadRegister()
    row0.set("1.2.3.4", 2000)
    row1 = HeadRegister()
    row1.set("6.7.8.9", 3000)
    t0= Register.set(row0)
    t1= Register.set(row1)
    print (Register.getrow(t1).IP)
