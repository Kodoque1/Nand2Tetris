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

import argparse
import re
import os

def enum(**enums):
    return type('Enum', (), enums)

TType=enum(KEYWORD = 1,SYMBOL = 2,IDENTIFIER = 3, INT_CONST = 4, STRING_CONST = 5)

list_keyword=["class","constructor","function","method","field","static","var"
            ,"int","char","boolean","void","true","false","null","this","let",
            "do","if","else","while","return"]

list_symbol=["{","}","(",")","[","]",".",",",";","+","-","*","/","&","|","<",">","=","~"]

list_op=["+","-","*","/","&","|","<",">","="]

list_unary=["-","~"]

escaped_character={"&" : "&amp;",
                    "<" : "&lt;",
                    ">" : "&gt;"}

def filter_commentary(s):
    return not (s=="" or s[0]=="/" or s[0]=="*")

def process_row(s):
    ret=[]
    for r in re.split("("+'|'.join(map(re.escape ,list_symbol))+")",s):
        tmp=r.strip()
        if tmp=='':
            pass
        elif tmp[0]=='"':
            ret.append(tmp)
        else:
            ret.extend(tmp.split())
    return ret


class JackTokenizer():
    def __init__(self,filename):
        tmp = filter(filter_commentary,map(str.strip,open(filename).readlines()))
        self.world_list=[]
        self.currentToken=""
        for r in tmp:
            #hack to handle // present in row
            for word in process_row(r.split("/")[0]):
                self.world_list.append(word)


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


class CompilationEngine():
    def __init__(self,input_file,output_file):
        self.depth=0
        self.input=JackTokenizer(input_file)
        self.output=open(output_file,"w")
        self.input.advance()
        print self.input.currentToken
        if((self.input.tokenType() is TType.KEYWORD) and (self.input.currentToken == "class")):
            print "Here!"
            self.CompileClass()
        self.output.close()

    def CompileClass(self):
        #Done
        print "In compile Class"
        self.output.write("  "*self.depth+"<class>\n")
        self.depth+=1
        self.output.write("  "*self.depth+"<keyword> class </keyword>\n")
        self.input.advance()
        if(self.input.tokenType()==TType.IDENTIFIER):
            self.output.write("  "*self.depth+"<identifier> "+self.input.identifier()+" </identifier>\n")
        self.input.advance()
        if (self.input.symbol() == "{"):
            self.output.write("  "*self.depth+" <symbol> { </symbol>\n")
        self.input.advance()
        while (self.input.tokenType() is TType.KEYWORD and self.input.currentToken in ["static","field"]):
            self.CompileClassVarDec()
        print self.input.currentToken
        while (self.input.tokenType() is TType.KEYWORD and self.input.currentToken in ["constructor","function","method"]):
            self.CompileSubRoutine()
        if (self.input.symbol() == "}"):
            self.output.write("  "*self.depth+"<symbol> } </symbol>\n")
        self.depth-=1
        self.output.write("  "*self.depth+"</class>\n")

    def CompileClassVarDec(self):
        #DONE
        self.output.write("  "*self.depth+"<classVarDec>\n")
        self.depth+=1
        #Writing the first "var"
        self.output.write("  "*self.depth+"<keyword> "+self.input.keyWord()+" </keyword>\n")
        self.input.advance()
        if (self.input.currentToken in ["int","char","boolean"]):
            self.output.write("  "*self.depth+"<keyword> "+self.input.keyWord()+" </keyword>\n")
        elif(self.input.tokenType() is TType.IDENTIFIER):
            self.output.write("  "*self.depth+"<identifier> "+self.input.identifier()+" </identifier>\n")
        self.input.advance()
        if(self.input.tokenType()==TType.IDENTIFIER):
            self.output.write("  "*self.depth+"<identifier> "+self.input.identifier()+" </identifier>\n")
        self.input.advance()
        while(self.input.symbol() == ","):
            self.output.write("  "*self.depth+"<symbol> , </symbol>\n")
            self.input.advance()
            if(self.input.tokenType()==TType.IDENTIFIER):
                self.output.write("  "*self.depth+"<identifier> "+self.input.identifier()+" </identifier>\n")
            self.input.advance()
        #Other VarName
        if (self.input.symbol() == ";"):
            self.output.write("  "*self.depth+"<symbol> ; </symbol>\n")
        self.input.advance()
        self.depth-=1
        self.output.write("  "*self.depth+"</classVarDec>\n")

    def CompileSubRoutine(self):
        #DONE
        self.output.write("  "*self.depth+"<subroutineDec>\n")
        self.depth+=1
        self.output.write("  "*self.depth+"<keyword> "+self.input.keyWord()+" </keyword>\n")
        self.input.advance()
        if (self.input.currentToken in ["void","int","char","boolean"]):
            self.output.write("  "*self.depth+" <keyword> "+self.input.keyWord()+" </keyword>\n")
        elif(self.input.tokenType() is TType.IDENTIFIER):
            self.output.write("  "*self.depth+"<identifier> "+self.input.identifier()+" </identifier>\n")
        self.input.advance()
        if(self.input.tokenType()==TType.IDENTIFIER):
            self.output.write("  "*self.depth+"<identifier> "+self.input.identifier()+" </identifier>\n")
        self.input.advance()
        if (self.input.symbol() == "("):
            self.output.write("  "*self.depth+"<symbol> ( </symbol>\n")
        self.input.advance()
        self.compileParameterList()
        print "in subroutine: " + self.input.currentToken
        if (self.input.symbol() == ")"):
            self.output.write("  "*self.depth+"<symbol> ) </symbol>\n")
        self.input.advance()
        self.output.write("  "*self.depth+"<subroutineBody>\n")
        self.depth+=1
        if (self.input.symbol() == "{"):
            self.output.write("  "*self.depth+"<symbol> { </symbol>\n")
        self.input.advance()
        while (self.input.currentToken == "var"):
            self.compileVarDec()
        self.compileStatements()
        if (self.input.symbol() == "}"):
            self.output.write("  "*self.depth+"<symbol> } </symbol>\n")
        self.depth-=1
        self.output.write("  "*self.depth+"</subroutineBody>\n")
        self.input.advance()
        self.depth-=1
        self.output.write("  "*self.depth+"</subroutineDec>\n")

    def compileStatements(self):
        #DONE; Warning next token will already be consumed with this function
        self.output.write("  "*self.depth+"<statements>\n")
        self.depth+=1
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
        self.depth-=1
        self.output.write("  "*self.depth+"</statements>\n")

    def compileIf(self):
        #Warning consume a token after use
        self.output.write("  "*self.depth+"<ifStatement>\n")
        self.depth+=1
        self.output.write("  "*self.depth+"<keyword> "+self.input.keyWord()+" </keyword>\n")
        self.input.advance()
        if (self.input.symbol() == "("):
            self.output.write("  "*self.depth+"<symbol> ( </symbol>\n")
        self.input.advance()
        self.compileExpression()
        if (self.input.symbol() == ")"):
            self.output.write("  "*self.depth+"<symbol> ) </symbol>\n")
        self.input.advance()
        if (self.input.symbol() == "{"):
            self.output.write("  "*self.depth+"<symbol> { </symbol>\n")
        self.input.advance()
        self.compileStatements()
        if (self.input.symbol() == "}"):
            self.output.write("  "*self.depth+"<symbol> } </symbol>\n")
        self.input.advance()
        if (self.input.symbol() == "else"):
            self.output.write("  "*self.depth+"<symbol> else </symbol>\n")
            self.input.advance()
            if (self.input.symbol() == "{"):
                self.output.write("  "*self.depth+"<symbol> { </symbol>\n")
            self.input.advance()
            self.compileStatements()
            if (self.input.symbol() == "}"):
                self.output.write("  "*self.depth+"<symbol> } </symbol>\n")
            self.input.advance()
        self.depth-=1
        self.output.write("  "*self.depth+"</ifStatement>\n")

    def compileLet(self):
        #DONE
        self.output.write("  "*self.depth+"<letStatement>\n")
        self.depth+=1
        self.output.write("  "*self.depth+"<keyword> "+self.input.keyWord()+" </keyword>\n")
        self.input.advance()
        if(self.input.tokenType()==TType.IDENTIFIER):
            self.output.write("  "*self.depth+"<identifier> "+self.input.identifier()+" </identifier>\n")
        self.input.advance()
        if(self.input.currentToken == "["):
            self.output.write("  "*self.depth+"<symbol> [ </symbol>\n")
            self.compileExpression()
            self.input.advance()
            if (self.input.symbol() == "]"):
                self.output.write("  "*self.depth+"<symbol> ] </symbol>\n")
            self.input.advance()
        if (self.input.symbol() == "="):
            self.output.write("  "*self.depth+"<symbol> = </symbol>\n")
        self.input.advance()
        self.compileExpression()
        if (self.input.symbol() == ";"):
            self.output.write("  "*self.depth+"<symbol> ; </symbol>\n")
        self.input.advance()
        self.depth-=1
        self.output.write("  "*self.depth+"</letStatement>\n")

    def compileExpression(self):
        #temp for compiler first phase
        self.output.write("  "*self.depth+"<expression>\n")
        self.depth+=1
        self.compileTerm()
        while(self.input.currentToken in list_op):
            self.output.write("  "*self.depth+"<symbol>" + self.input.symbol()+"</symbol>\n")
            self.input.advance()
            self.compileTerm()
        self.depth-=1
        self.output.write("  "*self.depth+"</expression>\n")

    def compileTerm(self):
        self.output.write("  "*self.depth+"<term>\n")
        self.depth+=1
        if (self.input.tokenType()==TType.INT_CONST):
            self.output.write("  "*self.depth+"<integerConstant> "+str(self.input.intVal())+" </integerConstant>\n")
            self.input.advance()
        elif (self.input.tokenType()==TType.STRING_CONST):
            self.output.write("  "*self.depth+"<StringConstant> "+self.input.stringVal()+" </StringConstant>\n")
            self.input.advance()
        elif (self.input.tokenType()==TType.KEYWORD):
            self.output.write("  "*self.depth+"<keyword> "+self.input.keyWord()+" </keyword>\n")
            self.input.advance()
        elif (self.input.tokenType()==TType.IDENTIFIER):
            self.output.write("  "*self.depth+"<identifier> "+self.input.identifier()+" </identifier>\n")
            self.input.advance()
            # Array
            if(self.input.currentToken=="["):
                self.output.write("  "*self.depth+"<symbol> "+self.input.symbol()+" </symbol>\n")
                self.input.advance()
                self.compileExpression()
                if(self.input()=="]"):
                    self.output.write("  "*self.depth+"<symbol> "+self.input.symbol()+" </symbol>\n")
                self.input.advance()
            #subroutineCall
            if (self.input.symbol() == "."):
                self.output.write("  "*self.depth+"<symbol> . </symbol>\n")
                self.input.advance()
                if(self.input.tokenType()==TType.IDENTIFIER):
                    self.output.write("  "*self.depth+"<identifier> "+self.input.identifier()+" </identifier>\n")
                self.input.advance()
            if (self.input.symbol() == "("):
                self.output.write("  "*self.depth+"<symbol> ( </symbol>\n")
                self.input.advance()
                self.compileExpressionList()
                if (self.input.symbol() == ")"):
                    self.output.write("  "*self.depth+"<symbol> ) </symbol>\n")
                self.input.advance()
        elif (self.input.symbol() == "("):
            self.output.write("  "*self.depth+"<symbol> ( </symbol>\n")
            self.input.advance()
            self.compileExpression()
            if (self.input.symbol() == ")"):
                self.output.write("  "*self.depth+"<symbol> ) </symbol>\n")
            self.input.advance()
        elif(self.input.symbol() in list_unary):
            print "unary"
            self.output.write("  "*self.depth+"<symbol>" +self.input.symbol() + "</symbol>\n")
            self.input.advance()
            self.compileTerm()
            # self.input.advance() --> very ugly!!
        self.depth-=1
        self.output.write("  "*self.depth+"</term>\n")


    def compileExpressionList(self):
        #Warning consume a token
        self.output.write("  "*self.depth+"<expressionList>\n")
        self.depth+=1
        if not (self.input.currentToken == ")"): #ugly
            self.compileExpression()
        while(self.input.symbol() == ","):
            self.output.write("  "*self.depth+"<symbol> , </symbol>\n")
            self.input.advance()
            self.compileExpression()
        self.depth-=1
        self.output.write("  "*self.depth+"</expressionList>\n")

    def compileParameterList(self):
        #DONE; warning consume a token at the end
        self.output.write("  "*self.depth+"<parameterList>\n")
        self.depth+=1
        if (self.input.currentToken in ["int","char","boolean"]):
            self.output.write("  "*self.depth+"<keyword> "+self.input.keyWord()+" </keyword>\n")
            self.input.advance()
        elif(self.input.tokenType() is TType.IDENTIFIER):
            self.output.write("  "*self.depth+"<identifier> "+self.input.identifier()+" </identifier>\n")
            self.input.advance()
        if(self.input.tokenType()==TType.IDENTIFIER):
            self.output.write("  "*self.depth+"<identifier> "+self.input.identifier()+" </identifier>\n")
            self.input.advance()
            while(self.input.symbol() == ","):
                self.output.write("  "*self.depth+"<symbol>,</symbol>\n")
                self.input.advance()
                if (self.input.currentToken in ["int","char","boolean"]):
                    self.output.write("  "*self.depth+"<keyword> "+self.input.keyWord()+" </keyword>\n")
                elif(self.input.tokenType() is TType.IDENTIFIER):
                    self.output.write("  "*self.depth+"<identifier> "+self.input.identifier()+" </identifier>\n")
                self.input.advance()
                if(self.input.tokenType()==TType.IDENTIFIER):
                    self.output.write("  "*self.depth+"<identifier> "+self.input.identifier()+" </identifier>\n")
                self.input.advance()
        self.depth-=1
        self.output.write("  "*self.depth+"</parameterList>\n")

    def compileVarDec(self):
        #DONE
        self.output.write("  "*self.depth+"<varDec>\n")
        self.depth+=1
        self.output.write("  "*self.depth+"<keyword> "+self.input.keyWord()+" </keyword>\n")
        self.input.advance()
        if (self.input.currentToken in ["int","char","boolean"]):
            self.output.write("  "*self.depth+"<keyword> "+self.input.keyWord()+" </keyword>\n")
        elif(self.input.tokenType() is TType.IDENTIFIER):
            self.output.write("  "*self.depth+"<identifier> "+self.input.identifier()+" </identifier>\n")
        self.input.advance()
        if(self.input.tokenType()==TType.IDENTIFIER):
            self.output.write("  "*self.depth+"<identifier> "+self.input.identifier()+" </identifier>\n")
        self.input.advance()
        while(self.input.symbol() == ","):
            self.output.write("  "*self.depth+"<symbol>,</symbol>\n")
            self.input.advance()
            if(self.input.tokenType()==TType.IDENTIFIER):
                self.output.write("  "*self.depth+"<identifier> "+self.input.identifier()+" </identifier>\n")
            self.input.advance()
        if(self.input.symbol() == ";"):
            self.output.write("  "*self.depth+"<symbol>;</symbol>\n")
        self.input.advance()
        self.depth-=1
        self.output.write("  "*self.depth+"</varDec>\n")

    def compileWhile(self):
        #DONE
        self.output.write("  "*self.depth+"<whileStatement>\n")
        self.depth+=1
        self.output.write("  "*self.depth+"<keyword> "+self.input.keyWord()+" </keyword>\n")
        self.input.advance()
        if (self.input.symbol() == "("):
            self.output.write("  "*self.depth+"<symbol> ( </symbol>\n")
        self.input.advance()
        self.compileExpression()
        if (self.input.symbol() == ")"):
            self.output.write("  "*self.depth+"<symbol> ) </symbol>\n")
        self.input.advance()
        if (self.input.symbol() == "{"):
            self.output.write("  "*self.depth+"<symbol> { </symbol>\n")
        self.input.advance()
        self.compileStatements()
        if (self.input.symbol() == "}"):
            self.output.write("  "*self.depth+"<symbol> } </symbol>\n")
        self.input.advance()
        self.depth-=1
        self.output.write("  "*self.depth+"</whileStatement>\n")

    def compileReturn(self):
        #DONE but hackish
        self.output.write("  "*self.depth+"<returnStatement>\n")
        self.depth+=1
        self.output.write("  "*self.depth+"<keyword> "+self.input.keyWord()+" </keyword>\n")
        self.input.advance()
        if (self.input.symbol() == ";"):
            self.output.write("  "*self.depth+"<symbol> ; </symbol>\n")
        else:
            self.compileExpression()
            if (self.input.symbol() == ";"):
                self.output.write("  "*self.depth+"<symbol> ; </symbol>\n")
        self.input.advance()
        self.depth-=1
        self.output.write("  "*self.depth+"</returnStatement>\n")

    def compileDo(self):
        #TODO
        self.output.write("  "*self.depth+"<doStatement>\n")
        self.depth+=1
        self.output.write("  "*self.depth+"<keyword> "+self.input.keyWord()+" </keyword>\n")
        self.input.advance()
        #subroutineCall
        if(self.input.tokenType()==TType.IDENTIFIER):
            self.output.write("  "*self.depth+"<identifier> "+self.input.identifier()+" </identifier>\n")
        self.input.advance()
        if (self.input.symbol() == "."):
            self.output.write("  "*self.depth+"<symbol> . </symbol>\n")
            self.input.advance()
            if(self.input.tokenType()==TType.IDENTIFIER):
                self.output.write("  "*self.depth+"<identifier> "+self.input.identifier()+" </identifier>\n")
            self.input.advance()
        if (self.input.symbol() == "("):
            self.output.write("  "*self.depth+"<symbol> ( </symbol>\n")
        self.input.advance()
        self.compileExpressionList()
        if (self.input.symbol() == ")"):
            self.output.write("  "*self.depth+"<symbol> ) </symbol>\n")
        self.input.advance()
        if (self.input.symbol() == ";"):
            self.output.write("  "*self.depth+"<symbol> ; </symbol>\n")
        self.input.advance()
        self.depth-=1
        self.output.write("  "*self.depth+"</doStatement>\n")
        pass

def main():
    #tokenizer test
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
                    co=CompilationEngine(jack_file,jack_file.split(".")[0]+".xml")
    else:
        print "in file"
        co=CompilationEngine(args.file,args.file.split(".")[0]+".xml")


if __name__ == '__main__':
    main()
