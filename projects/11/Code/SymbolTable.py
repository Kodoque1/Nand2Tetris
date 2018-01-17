import Config
TYPE=0
KIND=1
INDEX=2

class SymbolTable():
    def __init__(self):
        self.table={}
        self.ktable={Config.Kind.STATIC : 0,
                     Config.Kind.FIELD : 0,
                     Config.Kind.ARG : 0,
                     Config.Kind.VAR : 0}

    def startSubroutine(self):
        self.table={}
        self.ktable={Config.Kind.STATIC : 0,
                     Config.Kind.FIELD : 0,
                     Config.Kind.ARG : 0,
                     Config.Kind.VAR : 0}

    #index 0 : ctype, 1 : kind, 2 : index

    def Define(self,name,ctype,kind):
        self.ktable[kind]=self.ktable[kind]+1
        self.table[name] = [ctype,kind,self.ktable[kind]]

    def KindOf(self,name):
        if (name in self.table.keys()):
            return self.table[name][KIND]

    def TypeOf(self,name):
        if (name in self.table.keys()):
            return self.table[name][TYPE]

    def IndexOf(self,name):
        if (name in self.table.keys()):
            return self.table[name][INDEX]

    def VarCount(self,kind):
        return self.ktable[kind]

