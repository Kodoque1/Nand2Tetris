#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Makkron
#
# Created:     09/03/2014
# Copyright:   (c) Makkron 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

#from enum import Enum
import re

def enum(**enums):
    return type('Enum', (), enums)

##class CType(Enum):
##    A_COMMAND = 1
##    L_COMMAND = 2
##    C_COMMAND = 3

# un enum pour les diff?rents type de commande

CType=enum(A_COMMAND = 1,L_COMMAND = 2,C_COMMAND = 3)

# Ces dictonnaire vont servir ? faire la transcription des opcode en binaire

jmp_dict = {"":"000",
            "JGT":"001",
            "JEQ":"010",
            "JGE":"011",
            "JLT":"100",
            "JNE":"101",
            "JLE":"110",
            "JMP":"111"}

cmp_dict = {"0":"0101010",
            "1":"0111111",
            "-1":"0111010",
            "D":"0001100",
            "A":"0110000",
            "!D":"0001101",
            "!A":"0110001",
            "-D":"0001111",
            "-A":"0110011",
            "D+1":"0011111",
            "A+1":"0110111",
            "D-1":"0001110",
            "A-1":"0110010",
            "D+A":"0000010",
            "D-A":"0010011",
            "A-D":"0000111",
            "D&A":"0000000",
            "D|A":"0010101",
            "M":"1110000",
            "!M":"1110001",
            "-M":"1110011",
            "M+1":"1110111",
            "M-1":"1110010",
            "D+M":"1000010",
            "D-M":"1010011",
            "M-D":"1000111",
            "D&M":"1000000",
            "D|M":"1010101"}

class SymbolTable:
    def __init__(self):
        self.mapping = {"R0" : 0,
        "R1" : 1,
        "R2" : 2,
        "R3" : 3,
        "R4" : 4,
        "R5" : 5,
        "R6" : 6,
        "R7" : 7,
        "R8" : 8,
        "R9" : 9,
        "R10" : 10,
        "R11" : 11,
        "R12" : 12,
        "R13" : 13,
        "R14" : 14,
        "R15" : 15,
        "SCREEN" : 16384,
        "THAT" : 4,
        "KBD" : 24576,
        "THIS" : 3,
        "ARG" : 2,
        "LCL" : 1,
        "SP" : 0}

    def addEntry(self,symbol,address):
        self.mapping[symbol]=address

    def contains(self,symbol):
        return symbol in self.mapping

    def GetAdress(self,symbol):
        return self.mapping[symbol]

class Parser:
    def __init__(self,file):
        f = open(file)
        self.istream = filter(lambda x : not (x=="" or x[0:2]=="//"),map(str.strip,f.readlines()))
        #print self.istream

    def hasMoreCommands(self):
        return len(self.istream) > 0

    def advance(self):
        # IN : There are is still commands
        # OUT : current command gets updated
        if(self.hasMoreCommands()):
            self.currentCommand = self.istream.pop(0)

    def commandType(self):
        # IN :
        # OUT : returns the type of the current Command
        curr = self.currentCommand[0]
        if(curr == "@"):
            return CType.A_COMMAND
        elif(curr=="("):
            return CType.L_COMMAND
        else:
            return CType.C_COMMAND


    def symbol(self):
        # IN : A_COMMAND or L_COMMAND
        # OUT : Symbols of current command
        cType = self.commandType()
        if(cType == CType.A_COMMAND):
            return self.currentCommand[1:]
        if(cType == CType.L_COMMAND):
            return self.currentCommand[1:-1]

    def dest(self):
        # IN : C_COMMAND
        # OUT : returns dest mnemonic
        if (self.currentCommand.find("=") != -1):
            splitered = self.currentCommand.split("=")
            return splitered[0]
        else:
            return ""

    def comp(self):
        # IN : C_COMMAND
        # OUT : returns comp mnemonic
        splitered = self.currentCommand.split("=")
        return splitered[-1].split(";")[0]


    def jmp(self):
        # IN : C_COMMAND
        # OUT : returns jmp mnemonic
        if (self.currentCommand.find(";") != -1):
            splitered = self.currentCommand.split(";")
            return splitered[-1]
        else:
            return ""

def dest(cmd):
    return "".join([str(cmd.count(i)) for i in "ADM"])

def comp(cmd):
    return cmp_dict[cmd]

def jmp(cmd):
    return jmp_dict[cmd]

def main():
    pass

if __name__ == '__main__':
    p = Parser("Rect.asm")
    s = SymbolTable()
    f = open("output.hack","w")

    #First Pass
    mem_count = 0

    while(p.hasMoreCommands()):
        p.advance()
        if (p.commandType() == CType.L_COMMAND):
            if not (p.symbol().isdigit()):
                s.addEntry(p.symbol(),mem_count)
        else:
            mem_count+=1

    ##Second pass
    p = Parser("Rect.asm")
    var_count = 16

    while(p.hasMoreCommands()):
        p.advance()
        if (p.commandType() == CType.A_COMMAND):
            sym = p.symbol()
            if sym.isdigit():
                out = bin(int(sym))[2:].zfill(16) + "\n"
            else:
                if s.contains(sym):
                    out = bin(s.GetAdress(sym))[2:].zfill(16) + "\n"
                else:
                    s.addEntry(p.symbol(),var_count)
                    out = bin(var_count)[2:].zfill(16) + "\n"
                    var_count+=1
            f.write(out)

        elif (p.commandType() == CType.C_COMMAND):
            f.write("111" + comp(p.comp()) + dest(p.dest()) + jmp(p.jmp()) + "\n")

    print s.mapping


    f.close()

if __name__ == '__main__':
    main()


