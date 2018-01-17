#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      makkron
#
# Created:     19/02/2015
# Copyright:   (c) makkron 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

#TODO
# parse all compileEngine
# handle index for class variable
# void function : check type in function declaration and add in appropriate place (return or declaration?)
# use OS for alloc of object, how to deal with base reference of object?
# Does function must be in symbol table? (inelegant if not the case)

import argparse
import re
import os

#Define for table indexation

TYPE=0
KIND=1
INDEX=2

def enum(**enums):
    return type('Enum', (), enums)

TType=enum(KEYWORD = 1,SYMBOL = 2,IDENTIFIER = 3, INT_CONST = 4, STRING_CONST = 5)

SType=enum(CONST=1,LOCAL=2, POINTER = 3, ARG = 4, STATIC = 5, THIS = 6, THAT = 6, TEMP = 8)

AType=enum(ADD = 1, SUB = 2, NEG = 3, EQ = 4, GT = 5, LT = 6, AND = 7, OR = 8, NOT = 9)

Kind=enum(STATIC = 1, FIELD = 2, ARG = 3, VAR = 4)

list_keyword=["class","constructor","function","method","field","static","var"
            ,"int","char","boolean","void","true","false","null","this","let",
            "do","if","else","while","return"]

list_symbol=[" ","{","}","(",")","[","]",".",",",";","+","-","*","/","&","|","<",">","=","~","\""]

list_op=["+","-","*","/","&","|","<",">","="]

list_unary=["-","~"]

escaped_character={"&" : "&amp;",
                    "<" : "&lt;",
                    ">" : "&gt;"}

dict_segment={SType.CONST : "const",
              SType.LOCAL : "local",
              SType.POINTER : "pointer",
              SType.ARG : "argument",
              SType.STATIC : "static",
              SType.THIS : "this",
              SType.THAT : "that",
              SType.TEMP : "temp"}

dict_arithmetic={AType.ADD : "add",
                 AType.SUB : "sub",
                 AType.NEG : "neg",
                 AType.EQ : "eq",
                 AType.GT : "gt",
                 AType.LT : "lt",
                 AType.AND : "and",
                 AType.OR : "or",
                 AType.NOT : "not"}

#this whole affairs is embarassing ... all those mapping must be simplified

dict_bop={"+": AType.ADD,
         "-": AType.SUB,
         "&": AType.AND,
         "|": AType.OR,
         "<": AType.LT,
         ">": AType.GT,
         "=": AType.EQ}

dict_uop={"-": AType.NEG,
          "~": AType.NOT
}

#not sure if this mapping is accurate

dict_kind_to_segment = {Kind.ARG : SType.ARG,
                        Kind.STATIC : SType.STATIC,
                        Kind.FIELD : SType.THIS,
                        Kind.VAR : SType.LOCAL
}

def filter_commentary(s):
    return not (s=="" or s[0]=="/" or s[0]=="*")

def filter_whitespace(s):
    return re.match("^\ *$",s) is None

def process_row(s):
    ret=[]
    buffering=False
    buf=""
    preprocessed=re.split("("+'|'.join(map(re.escape ,list_symbol))+")",s)
    #print preprocessed
    for r in preprocessed:
        if buffering:
            if r=='':
                pass
            elif r=='"':
                buf=buf+r
                ret.append(buf)
                buffering=False
                buf=""
            else:
                buf=buf+r
        else:
            if r=='':
                pass
            elif r=='"':
                buf=buf+r
                buffering=True
            else:
                ret.append(r)
    return ret

def match_whitespace(s):
    return not (re.match())
class SymbolTable():
    def __init__(self):
        self.table={}
        self.ktable={Kind.STATIC : 0,
                     Kind.FIELD : 0,
                     Kind.ARG : 0,
                     Kind.VAR : 0}

    def startSubroutine(self):
        self.table={}
        self.ktable={Kind.STATIC : 0,
                     Kind.FIELD : 0,
                     Kind.ARG : 0,
                     Kind.VAR : 0}

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

class JackTokenizer():
    def __init__(self,f):
        tmp = filter(filter_commentary,map(str.strip,f.readlines()))
        self.world_list=""
        self.currentToken=""
        for r in tmp:
            com=r.find("//")
            if com != -1:
                self.world_list=self.world_list + r[0:com]
            else:
                self.world_list=self.world_list + r
        #print self.world_list
        self.world_list=process_row(self.world_list)
        self.world_list=filter(filter_whitespace,self.world_list)
        print self.world_list

    def hasMoreTokens(self):
        return len(self.world_list) > 0

    def advance(self):
        if self.hasMoreTokens():
            self.currentToken=self.world_list.pop(0)

    def tokenType(self):
        if (self.currentToken in list_keyword):
            return TType.KEYWORD
        elif (self.currentToken in list_symbol):
            return TType.SYMBOL
        elif (self.currentToken.isdigit()):
            tmp=int(self.currentToken)
            if tmp >= 0 and tmp < 32767:
                return TType.INT_CONST
        elif self.currentToken[0]=='"' and self.currentToken[-1]=='"':
            if not ('"' in self.currentToken[1:-1]):
                print self.currentToken[-1]
                return TType.STRING_CONST
        else:
            return TType.IDENTIFIER

    def symbol(self):
        if (self.tokenType()==TType.SYMBOL):
            tmp = self.currentToken
            if (tmp in escaped_character.keys()):
                return escaped_character[tmp]
            else:
                return self.currentToken

    def identifier(self):
        if (self.tokenType()==TType.IDENTIFIER):
            return self.currentToken

    def intVal(self):
        if (self.tokenType()==TType.INT_CONST):
            return int(self.currentToken)

    def stringVal(self):
        if (self.tokenType()==TType.STRING_CONST):
            return self.currentToken[1:-1]

    def keyWord(self):
        if (self.tokenType()==TType.KEYWORD):
            return self.currentToken

class VMWriter:
    def __init__(self,output):
        self.output=open(output,"w")

    def writePush(self,segment,index):
        self.output.write("push " + str(dict_segment[segment]) + " " + str(index) +"\n")

    def writePop(self,segment,index):
        self.output.write("pop " + str(dict_segment[segment]) + " " + str(index) +"\n")

    def WriteArithmetic(self,command):
        #print command
        self.output.write(str(dict_arithmetic[command])+"\n")

    def WriteLabel(self,label):
        self.output.write("label " + str(label) + "\n")

    def WriteGoto(self,label):
        self.output.write("goto " + str(label) + "\n")

    def WriteIf(self,label):
        self.output.write("goto " + str(label) + "\n")

    def WriteCall(self,name,nArgs):
        self.output.write("call " + str(name) + " " + str(nArgs) + "\n")

    def WriteFunction(self,name,nLocals):
        self.output.write("function " + str(name) + " " + str(nLocals) + "\n")

    def writeReturn(self):
        self.output.write("return\n")

    def close(self):
        self.output.close()

class CompilationEngine():
    def __init__(self,input_file,output_file):

        # handle input and output
        self.input=JackTokenizer(input_file)
        self.output=VMWriter(output_file)

        # H
        self.labelCounter=0
        self.className=""
        #initialize Scope table
        self.classScope=SymbolTable()
        self.routineScope=SymbolTable()

        # Start parsing
        self.input.advance()
        print self.input.currentToken
        if((self.input.tokenType() is TType.KEYWORD) and (self.input.currentToken == "class")):
            print "Beginning compilation"
            self.input.advance()
            self.CompileClass()
        self.output.close()

    def CompileClass(self):
        #Done
        print "In compile Class"
        if(self.input.tokenType()==TType.IDENTIFIER):
            self.className=self.input.currentToken
        self.input.advance()
        if (self.input.symbol() == "{"):
            pass
        self.input.advance()
        self.nField=0;
        while (self.input.tokenType() is TType.KEYWORD and self.input.currentToken in ["static","field"]):
            self.CompileClassVarDec()
            self.nField=self.nField+1
        print self.input.currentToken
        while (self.input.tokenType() is TType.KEYWORD and self.input.currentToken in ["constructor","function","method"]):
            self.CompileSubRoutine()
        if (self.input.symbol() == "}"):
            pass

    def CompileClassVarDec(self):
        #DONE
        #Writing the first "var"
        if (self.input.currentToken=="static"):
            kind=Kind.STATIC
        else:
            kind=Kind.FIELD
        self.input.advance()
        if (self.input.currentToken in ["int","char","boolean"]):
            ctype=self.input.currentToken
        elif(self.input.tokenType() is TType.IDENTIFIER):
            ctype=self.input.currentToken
        self.input.advance()
        if(self.input.tokenType()==TType.IDENTIFIER):
            self.classScope.Define(self.input.currentToken, ctype, kind)
        self.input.advance()
        while(self.input.symbol()== ","):
            self.input.advance()
            if(self.input.tokenType()==TType.IDENTIFIER):
                self.classScope.Define(self.input.currentToken, ctype, kind)
            self.input.advance()
        #Other VarName
        if (self.input.symbol() == ";"):
            pass
        self.input.advance()

    def CompileSubRoutine(self):
        #DONE
        constructor=False
        method=False
        if(self.input.currentToken=="constructor"):
            constructor=True
        elif(self.input.currentToken=="method"):
            method=True
        self.routineScope.startSubroutine()
        self.input.advance()
        void=False
        if (self.input.currentToken in ["int","char","boolean"]):
            pass
        elif(self.input.tokenType() is TType.IDENTIFIER):
            pass
        self.input.advance()
        if(self.input.tokenType()==TType.IDENTIFIER):
            name=self.input.currentToken
        self.input.advance()
        if (self.input.symbol() == "("):
            pass
        self.input.advance()
        #insert into routineTables all the arg and retrieve their number
        self.routineScope.startSubroutine()
        self.compileParameterList()
        if (self.input.symbol() == ")"):
            pass
        self.input.advance()
        if (self.input.symbol() == "{"):
            pass
        self.input.advance()
        nlocal=0
        while (self.input.currentToken == "var"):
            nlocal=self.compileVarDec()+nlocal
            self.input.advance()
        if(method):
            self.output.WriteFunction(self.className+"."+name,nlocal+1)
        else:
            self.output.WriteFunction(self.className+"."+name,nlocal)
        if (constructor):
            self.output.WriteCall("Memory.alloc",self.nField)
            self.output.writePop(SType.POINTER,0)
        self.compileStatements()
        if (self.input.symbol() == "}"):
            pass
        self.input.advance()

    def compileStatements(self):
        #DONE; Warning next token will already be consumed with this function
        while(self.input.currentToken in ["let","if","while","do","return"]):
            if self.input.keyWord() == "let":
                self.compileLet()
            elif(self.input.keyWord() == "if"):
                self.compileIf()
            elif(self.input.keyWord() == "while"):
                self.compileWhile()
            elif(self.input.keyWord() == "do"):
                self.compileDo()
            elif(self.input.keyWord() == "return"):
                self.compileReturn()

    #Control flow
    def compileWhile(self):
        #DONE
        self.input.advance()
        tmp=self.labelCounter
        self.output.WriteLabel("label."+str(self.labelCounter))
        self.labelCounter=self.labelCounter+1
        if (self.input.symbol() == "("):
            pass
        #print self.input.currentToken
        self.input.advance()
        self.compileExpression()
        if (self.input.symbol() == ")"):
            pass
        self.output.WriteArithmetic(AType.NOT)
        self.output.WriteIf("label."+str(self.labelCounter))
        self.input.advance()
        if (self.input.symbol() == "{"):
            pass
        self.input.advance()
        self.compileStatements()
        if (self.input.symbol() == "}"):
            pass
        self.output.WriteGoto(tmp)
        self.output.WriteLabel("label."+str(self.labelCounter))
        self.labelCounter=self.labelCounter+1
        self.input.advance()

    def compileIf(self):
        #DONE; Warning consume a token after use
        self.input.advance()
        if (self.input.symbol() == "("):
            pass
        self.input.advance()
        self.compileExpression()
        #code for ~cond
        self.output.WriteArithmetic(AType.NOT)
        if (self.input.symbol() == ")"):
            pass
        self.output.WriteIf("label."+str(self.labelCounter))
        self.input.advance()
        if (self.input.symbol() == "{"):
            pass
        self.input.advance()
        self.compileStatements()
        if (self.input.symbol() == "}"):
            pass
        self.input.advance()
        self.output.WriteGoto("label."+str(self.labelCounter+1))
        self.output.WriteLabel("label."+str(self.labelCounter))
        self.labelCounter+=1
        if (self.input.symbol() == "else"):
            pass
            self.input.advance()
            if (self.input.symbol() == "{"):
                pass
            self.input.advance()
            self.compileStatements()
            if (self.input.symbol() == "}"):
                pass
            self.input.advance()
        self.output.WriteLabel("label."+str(self.labelCounter))
        self.labelCounter+=1

    def compileLet(self):
        #DONE
        self.input.advance()
        name=self.input.currentToken
        (segment,index,ctype)=self.get_segment(name)
        self.output.writePush(segment,index)
        self.input.advance()
        if(self.input.currentToken == "["):
            #print self.input.currentToken
            self.input.advance()
            self.compileExpression()
            print "before add:" + self.input.currentToken
            if (self.input.currentToken == "]"):
                print "add"
                self.output.WriteArithmetic(AType.ADD)
            self.input.advance()
        self.output.writePop(SType.POINTER,1)
        if (self.input.symbol() == "="):
            pass
        print self.input.currentToken
        self.input.advance()
        self.compileExpression()
        print "finishing let"
        print self.input.currentToken
        if (self.input.symbol() == ";"):
            self.output.writePop(SType.THAT,0)
        self.input.advance()

    def compileExpression(self):
        #DONE; temp for compiler first phase
        self.compileTerm()
        op=self.input.currentToken
        print op
        if(op in list_op):
            self.input.advance()
            self.compileTerm()
            if op=="*":
                print "calling multiply"
                self.output.WriteCall("Math.multiply",2)
            elif op=="/":
                self.output.WriteCall("Math.divide",2)
            else:
                #print self.input.currentToken

                self.output.WriteArithmetic(dict_bop[op])
            #self.compileExpression()

    def compileTerm(self):
        #DONE
        if (self.input.tokenType()==TType.INT_CONST):
            print "int:" + str(self.input.tokenType())
            self.output.writePush(SType.CONST,int(self.input.currentToken))
            self.input.advance()
        elif (self.input.tokenType()==TType.STRING_CONST):
            #touchy
            const=self.input.currentToken
            print const
            self.output.writePush(SType.CONST,len(const))
            self.output.WriteCall("String.new",1)
            for c in const[1:-1]:
                print "Write call :" + self.input.currentToken
                self.output.WriteCall("String.appendChar",ord(c))
            self.input.advance()
        elif (self.input.tokenType()==TType.KEYWORD):
            #TODO true,false,null,this
            kw=self.input.currentToken
            if (kw=="this"):
                self.output.writePush(SType.POINTER,0)
            elif (kw in ["null","false"]):
                self.output.writePush(SType.CONST,0)
            elif (kw=="false"):
                self.output.writePush(SType.CONST,1)
                self.output.WriteArithmetic(AType.NEG)
            self.input.advance()
        elif (self.input.tokenType()==TType.IDENTIFIER):
            identifier=self.input.currentToken
            if ((self.classScope.KindOf(identifier) is None) and (self.routineScope.KindOf(identifier) is None)):
                self.input.advance()
                print "before function call"
                if (self.input.symbol() == "."):
                        print "function call:"
                        self.input.advance()
                        if(self.input.tokenType()==TType.IDENTIFIER):
                            pass
                        method=self.input.currentToken
                        self.input.advance()
                        if (self.input.symbol() == "("):
                            self.input.advance()
                            nArg=self.compileExpressionList()
                            if (self.input.symbol() == ")"):
                                pass
                            self.output.WriteCall(identifier+"."+method,nArg)
                            self.input.advance()
            # Array
            else:
                (segment,index,ctype)=self.get_segment(identifier)
                self.input.advance()
                if (self.input.symbol() == "("):
                    self.input.advance()
                    nArg=self.compileExpressionList()
                    if (self.input.symbol() == ")"):
                        pass
                    self.output.WriteCall(identifier,nArg)
                    self.input.advance()
                else:
                    self.output.writePush(segment,index)
                    if(self.input.currentToken=="["):
                        self.input.currentToken
                        self.input.advance()
                        self.compileExpression()
                        if(self.input.currentToken=="]"):
                            pass
                        print "in expression :" + self.input.currentToken
                        self.output.WriteArithmetic(AType.ADD)
                        self.output.writePush(SType.POINTER,1)
                        self.output.writePop(SType.TEMP,0)
                        self.output.writePop(SType.POINTER,1)
                        self.output.writePush(SType.THAT,0)
                        self.input.advance()
                        print "after array: " + str(self.input.currentToken)
                    #subroutineCall
                    if (self.input.symbol() == "."):
                        self.input.advance()
                        if(self.input.tokenType()==TType.IDENTIFIER):
                            pass
                        method=self.input.currentToken
                        self.input.advance()
                        if (self.input.symbol() == "("):
                            self.input.advance()
                            nArg=self.compileExpressionList()
                            if (self.input.symbol() == ")"):
                                pass
                            self.output.WriteCall(identifier+"."+method,nArg+1)
                            self.input.advance()
        elif (self.input.symbol() == "("):
            self.input.advance()
            self.compileExpression()
            if (self.input.symbol() == ")"):
                pass
                self.input.advance()
        elif(self.input.symbol() in list_unary):
            print "test"
            uop=self.input.currentToken
            #print uop
            self.input.advance()
            self.compileTerm()
            print "stuff"
            self.output.WriteArithmetic(dict_uop[uop])

    def compileExpressionList(self):
        #DONE; Warning consume a token
        nArg=0
        if not (self.input.currentToken == ")"): #ugly
            self.compileExpression()
            nArg=1
        while(self.input.symbol() == ","):
            self.input.advance()
            self.compileExpression()
            nArg=nArg+1
        return nArg

    def compileParameterList(self):
        #DONE; warning consume a token at the end
        #Declare in the subRoutineScope as arg
        kind=Kind.ARG
        if (self.input.currentToken in ["int","char","boolean"]):
            ctype=self.input.currentToken
            self.input.advance()
        elif(self.input.tokenType() is TType.IDENTIFIER):
            ctype=self.input.currentToken
            self.input.advance()
        if(self.input.tokenType()==TType.IDENTIFIER):
            self.routineScope.Define(self.input.currentToken,ctype,kind)
            self.input.advance()
            while(self.input.symbol() == ","):
                self.input.advance()
                if (self.input.currentToken in ["int","char","boolean"]):
                    ctype=self.input.currentToken
                elif(self.input.tokenType() is TType.IDENTIFIER):
                    ctype=self.input.currentToken
                self.input.advance()
                if(self.input.tokenType()==TType.IDENTIFIER):
                    self.routineScope.Define(self.input.currentToken,ctype,kind)
                self.input.advance()
        return

    def compileVarDec(self):
        #DONE
        nlocal=0
        kind=Kind.VAR
        self.input.advance()
        if (self.input.currentToken in ["int","char","boolean"]):
            ctype=self.input.currentToken
        elif(self.input.tokenType() is TType.IDENTIFIER):
            ctype=self.input.currentToken
        self.input.advance()
        if(self.input.tokenType()==TType.IDENTIFIER):
            self.routineScope.Define(self.input.currentToken,ctype,kind)
        nlocal=1
        self.input.advance()
        while(self.input.symbol() == ","):
            self.input.advance()
            if(self.input.tokenType()==TType.IDENTIFIER):
                self.routineScope.Define(self.input.currentToken,ctype,kind)
            self.input.advance()
            nlocal=nlocal+1
        if(self.input.symbol() == ";"):
            pass
        return nlocal



    def compileReturn(self):
        #DONE but hackish
        self.input.advance()
        if (self.input.symbol() == ";"):
            self.output.writePush(SType.CONST,0)
            self.output.writeReturn()
        else:
            self.compileExpression()
            if (self.input.symbol() == ";"):
                self.output.writeReturn()
        self.input.advance()

    def compileDo(self):
        #DONE
        self.input.advance()
        #subroutineCall
        nArg=0
        if(self.input.tokenType()==TType.IDENTIFIER):
            pass
        name=self.input.currentToken
        self.input.advance()
        if (self.input.symbol() == "."):
            (segment,index,ctype)=self.get_segment(name)
            self.input.advance()
            if(self.input.tokenType()==TType.IDENTIFIER):
                pass
            name=ctype+"."+self.input.currentToken
            self.output.writePush(segment,index)
            nArg=1
            self.input.advance()
        if (self.input.symbol() == "("):
            pass
        self.input.advance()
        nArg=self.compileExpressionList()+nArg
        if (self.input.symbol() == ")"):
            pass
        self.input.advance()
        if (self.input.symbol() == ";"):
            pass
        self.output.WriteCall(name,nArg)
        self.output.writePop(SType.TEMP,0)
        self.input.advance()

    def get_segment(self,name):
        print "name: " + name
        print "routineScope: " + str(self.routineScope.table)
        segment=dict_kind_to_segment[self.routineScope.KindOf(name)]
        if segment:
            index=self.routineScope.IndexOf(name)
            ctype=self.routineScope.TypeOf(name)
            #should check in classScope, but since there is no error handling
        else:
            segment=dict_kind_to_segment(self.classScope.KindOf(name))
            index=self.classScope.IndexOf(name)
            ctype=self.routineScope.TypeOf(name)
        return (segment,index,ctype)


def main():
    #Selecting Input
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-d",dest="directory")
    group.add_argument("-f",dest="file")
    args=parser.parse_args()
    print "Entered prog"
    #code to select between two modes
    if args.file is None:
        for (dirpath, dirnames, filenames) in os.walk(args.directory):
            for filename in filenames:
                if filename[-5:] == '.jack':
                    jack_file = os.sep.join([dirpath, filename])
                    co=CompilationEngine(open(jack_file),jack_file.split(".")[0]+".vm")
    else:
        print "in file"
        co=CompilationEngine(open(args.file),args.file.split(".")[0]+".vm")


if __name__ == '__main__':
    main()
