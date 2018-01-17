#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      bla
#
# Created:     14/12/2015
# Copyright:   (c) bla 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import Config
import JackTokenizer
import OutputEngine
import traceback
import sys
import SymbolTable
import VMWriter

class CompilationEngine():

    def __init__(self,finput,foutput,debugmode):
        self.out=VMWriter.VMWriter(foutput)
        self.tokenizer=JackTokenizer.JackTokenizer(finput)
        self.varCount=0;
        self.argCount=0;
        self.void_functions=[];
        self.class_name="";

        # Sym tables initialization
        self.class_sym_table=SymbolTable.SymbolTable()
        self.function_sym_table=SymbolTable.SymbolTable()

        self.tokenizer.advance()
        if not debugmode:
            try:
                self.CompileClass()
            except Exception as e:
                traceback.print_exc(file=sys.stdout)
                print e
            self.out.close()

    def CompileClass(self):

        if not (self.tokenizer.tokenType() == Config.TType.KEYWORD and self.tokenizer.keyword() == "class"):
            raise Exception("Syntax Error; expected \"class\" instead of:" + self.tokenizer.currentToken)

        self.tokenizer.advance()
        if not(self.tokenizer.tokenType() == Config.TType.IDENTIFIER):
            raise Exception("Syntax Error; expected identifier instead of:" + self.tokenizer.currentToken)

        self.class_name=self.tokenizer.currentToken
        self.tokenizer.advance()
        if not(self.tokenizer.tokenType() == Config.TType.SYMBOL and self.tokenizer.keyword() == "{"):
            raise Exception("Syntax Error; expected \"{\" instead of:" + self.tokenizer.currentToken)

        self.tokenizer.advance()
        while self.tokenizer.tokenType() == Config.TType.KEYWORD and self.tokenizer.keyword() in ["static","field"]:
            self.CompileClassVarDec()
        while self.tokenizer.tokenType() == Config.TType.KEYWORD and self.tokenizer.keyword() in ["constructor","function","method"]:
            self.CompileSubroutine()
        if not(self.tokenizer.tokenType() == Config.TType.SYMBOL and self.tokenizer.keyword() == "}"):
            raise Exception("Syntax Error; expected \"}\" instead of:" + self.tokenizer.currentToken)


    def CompileClassVarDec(self):
        JackType=""
        Kind=""

        self.out.writeBeginningTag("classVarDec")
        if not (self.tokenizer.tokenType() == Config.TType.KEYWORD and self.tokenizer.keyword() in ["static","field"]):
            raise Exception("Syntax Error; expected \"static\" or \"field\" instead of:" + self.tokenizer.currentToken)

        Kind=self.tokenizer.keyword()
        self.tokenizer.advance()
        if self.tokenizer.tokenType() == Config.TType.KEYWORD and self.tokenizer.keyword() in ["int","char","boolean"]:

            JackType=self.tokenizer.keyword()
        elif self.tokenizer.tokenType() == Config.TType.IDENTIFIER:

            JackType=self.tokenizer.identifier()
        else:
            raise Exception("Syntax Error; expected primitive type or class instead of:" + self.tokenizer.currentToken)
        self.tokenizer.advance()
        if not (self.tokenizer.tokenType() == Config.TType.IDENTIFIER):
            raise Exception("Syntax Error; expected identifier instead of:" + self.tokenizer.currentToken)
        self.class_sym_table.Define(self.tokenizer.identifier(),JackType,Kind)

        self.tokenizer.advance()
        while self.tokenizer.tokenType() == Config.TType.SYMBOL and self.tokenizer.symbol() == ",":

            self.tokenizer.advance()
            if not (self.tokenizer.tokenType() == Config.TType.IDENTIFIER):
                raise Exception("Syntax Error; expected identifier instead of:" + self.tokenizer.currentToken)

            class_sym_table.Define(self.tokenizer.identifier(),JackType,Kind)
            self.tokenizer.advance()
        if not(self.tokenizer.tokenType() == Config.TType.SYMBOL and self.tokenizer.symbol() == ";"):
            raise Exception("Syntax Error; expected \";\" instead of: " + self.tokenizer.currentToken)

        self.tokenizer.advance()



    def CompileVarDec(self):

        JackType=""

        self.varCount=self.varCount+1
        if not(self.tokenizer.tokenType() == Config.TType.KEYWORD and self.tokenizer.keyword() == "var"):
            raise Exception("Syntax Error; expected var instead of: " + self.tokenizer.currentToken)

        self.tokenizer.advance();
        if self.tokenizer.tokenType() == Config.TType.KEYWORD and self.tokenizer.keyword() in ["int","char","boolean"]:

            JackType=self.tokenizer.keyword()
        elif self.tokenizer.tokenType() == Config.TType.IDENTIFIER:

            JackType=self.tokenizer.identifier()
        else:
            raise Exception("Syntax Error; expected primitive type or class instead of:" + self.tokenizer.currentToken)
        self.tokenizer.advance()
        if not (self.tokenizer.tokenType() == Config.TType.IDENTIFIER):
            raise Exception("Syntax Error; expected identifier instead of:" + self.tokenizer.currentToken)

        self.function_sym_table.Define(self.tokenizer.identifier(),JackType,Config.Kind.VAR)
        self.tokenizer.advance()
        while self.tokenizer.tokenType() == Config.TType.SYMBOL and self.tokenizer.symbol() == ",":
            self.varCount=self.varCount+1
            self.tokenizer.advance()
            if not (self.tokenizer.tokenType() == Config.TType.IDENTIFIER):
                raise Exception("Syntax Error; expected identifier instead of:" + self.tokenizer.currentToken)

            self.function_sym_table.Define(self.tokenizer.identifier(),JackType,Config.Kind.VAR)
            self.tokenizer.advance()
        if not(self.tokenizer.tokenType() == Config.TType.SYMBOL and self.tokenizer.symbol() == ";"):
            raise Exception("Syntax Error; expected \";\" instead of: " + self.tokenizer.currentToken)

        self.tokenizer.advance()


    def CompileParameterList(self):
        JackType=""

        if not(self.tokenizer.tokenType() == Config.TType.SYMBOL and self.tokenizer.symbol() == ")"):

            if self.tokenizer.tokenType() == Config.TType.KEYWORD and self.tokenizer.keyword() in ["int","char","boolean"]:

                JackType=self.tokenizer.keyword()
            elif self.tokenizer.tokenType() == Config.TType.IDENTIFIER:

                JackType=self.tokenizer.identifier()
            else:
                raise Exception("Syntax Error; expected primitive type or class instead of:" + self.tokenizer.currentToken)
            self.tokenizer.advance()
            if not (self.tokenizer.tokenType() == Config.TType.IDENTIFIER):
                raise Exception("Syntax Error; expected identifier instead of:" + self.tokenizer.currentToken)

            self.function_sym_table.Define(self.tokenizer.identifier(),JackType,Config.Kind.Arg)
            self.tokenizer.advance()
            while self.tokenizer.tokenType() == Config.TType.SYMBOL and self.tokenizer.symbol() == ",":

                self.tokenizer.advance()
                if self.tokenizer.tokenType() == Config.TType.KEYWORD and self.tokenizer.keyword() in ["int","char","boolean"]:

                    JackType=self.tokenizer.keyword()
                elif self.tokenizer.tokenType() == Config.TType.IDENTIFIER:

                    JackType=self.tokenizer.identifier()
                else:
                    raise Exception("Syntax Error; expected primitive type or class instead of:" + self.tokenizer.currentToken)
                self.tokenizer.advance()
                if not (self.tokenizer.tokenType() == Config.TType.IDENTIFIER):
                    raise Exception("Syntax Error; expected identifier instead of:" + self.tokenizer.currentToken)

                self.function_sym_table.Define(self.tokenizer.identifier(),JackType,Config.Kind.Arg)
                self.tokenizer.advance()


    def CompileExpression(self):

        self.CompileTerm()
        while self.tokenizer.tokenType() == Config.TType.SYMBOL and self.tokenizer.symbol() in Config.list_op:
            tmp=self.tokenizer.symbol()
            self.tokenizer.advance()
            self.CompileTerm()
            if tmp=="*":
                self.out.WriteCall("Math.multiply",2)
            elif tmp=="/":
                self.out.WriteCall("Math.divide",2)
            else:
                self.out.WriteArithmetic(Config.dict_bop[tmp])


    def CompileTerm(self):

        if self.tokenizer.tokenType() == Config.TType.STRING_CONST:

            self.tokenizer.advance()
        elif self.tokenizer.tokenType() == Config.TType.INT_CONST:
            self.out.writePush(Config.SType.CONST,self.tokenizer.intVal())
            self.tokenizer.advance()
        elif self.tokenizer.tokenType() == Config.TType.KEYWORD:

            self.tokenizer.advance()
        elif self.tokenizer.tokenType() == Config.TType.SYMBOL and self.tokenizer.symbol() == "(":

            self.tokenizer.advance()
            self.CompileExpression()
            if not(self.tokenizer.tokenType() == Config.TType.SYMBOL and self.tokenizer.symbol() == ")"):
                raise Exception("Syntax Error; expected ) instead of:" + self.tokenizer.currentToken)

            self.tokenizer.advance()
        elif self.tokenizer.tokenType() == Config.TType.SYMBOL and self.tokenizer.symbol() in Config.list_unary:

            self.tokenizer.advance()
            self.CompileTerm()
        elif self.tokenizer.tokenType() == Config.TType.IDENTIFIER:
            idt=self.tokenizer.identifier()
            if not (self.function_sym_table.KindOf(idt) is None):
                pass
            else:
                pass
            self.tokenizer.advance()
            if self.tokenizer.tokenType() == Config.TType.SYMBOL and self.tokenizer.symbol() in [".","("]:
                if self.tokenizer.tokenType() == Config.TType.SYMBOL and self.tokenizer.symbol() == ".":

                    self.tokenizer.advance()
                    if not(self.tokenizer.tokenType() == Config.TType.IDENTIFIER):
                        raise Exception("Syntax Error; expected identifier instead of:" + self.tokenizer.currentToken)
                    idt=self.tokenizer.identifier()
                    if not (self.function_sym_table.KindOf(idt) is None):
                        pass
                    else:
                        pass
                    self.tokenizer.advance()
                if not(self.tokenizer.tokenType() == Config.TType.SYMBOL and self.tokenizer.symbol() == "("):
                    raise Exception("Syntax Error; expected ( instead of:" + self.tokenizer.currentToken)

                self.tokenizer.advance()
                self.CompileExpressionList()
                if not(self.tokenizer.tokenType() == Config.TType.SYMBOL and self.tokenizer.symbol() == ")"):
                    raise Exception("Syntax Error; expected ) instead of:" + self.tokenizer.currentToken)

                self.tokenizer.advance()
            elif self.tokenizer.tokenType() == Config.TType.SYMBOL and self.tokenizer.symbol() == "[":

                self.tokenizer.advance()
                self.CompileExpression()
                if not(self.tokenizer.tokenType() == Config.TType.SYMBOL and self.tokenizer.symbol() == "]"):
                    raise Exception("Syntax Error; expected ) instead of:" + self.tokenizer.currentToken)

                self.tokenizer.advance()
        else:
            raise Exception("Syntax Error; expected term instead of:" + self.tokenizer.currentToken)


    def CompileExpressionList(self):

        if not(self.tokenizer.tokenType() == Config.TType.SYMBOL and self.tokenizer.symbol() == ")"):
            self.CompileExpression()
            self.argCount=self.argCount+1
            while self.tokenizer.tokenType() == Config.TType.SYMBOL and self.tokenizer.symbol() == ",":
                self.argCount=self.argCount+1
                self.tokenizer.advance()
                self.CompileExpression()


    def CompileReturn(self):

        if not(self.tokenizer.tokenType() == Config.TType.KEYWORD and self.tokenizer.keyword() == "return"):
            raise Exception("Syntax Error; expected \"return\" instead of:" + self.tokenizer.currentToken)

        self.tokenizer.advance()
        if not(self.tokenizer.tokenType() == Config.TType.SYMBOL and self.tokenizer.symbol() == ";"):
            self.CompileExpression()
        if not(self.tokenizer.tokenType() == Config.TType.SYMBOL and self.tokenizer.symbol() == ";"):
            raise Exception("Syntax Error; expected \";\" instead of:" + self.tokenizer.currentToken)
        if self.isVoid:
            self.out.writePush(Config.SType.CONST,0)
        self.out.writeReturn()
        self.tokenizer.advance()


    def CompileLet(self):

        if not(self.tokenizer.tokenType() == Config.TType.KEYWORD and self.tokenizer.symbol() == "let"):
            raise Exception("Syntax Error; expected let instead of:" + self.tokenizer.currentToken)

        self.tokenizer.advance()
        if not(self.tokenizer.tokenType() == Config.TType.IDENTIFIER):
            raise Exception("Syntax Error; expected identifier instead of:" + self.tokenizer.currentToken)
        idt=self.tokenizer.identifier()
        #putting the value or array pointer on the stack
        if not (self.function_sym_table.KindOf(idt) is None):
            self.out.writePush(self.function_sym_table.KindOf(idt),self.function_sym_table.IndexOf(idt))
        elif not (self.class_sym_table.KindOf(idt) is None):
            self.out.writePush(self.class_sym_table.KindOf(idt),self.class_sym_table.IndexOf(idt))
        else:
            raise Exception("Unknown identifier: " + self.tokenizer.currentToken)
        self.tokenizer.advance()
        self.out.writePush()
        if self.tokenizer.tokenType() == Config.TType.SYMBOL and self.tokenizer.symbol() == "[":

            self.tokenizer.advance()
            self.CompileExpression()
            if not(self.tokenizer.tokenType() == Config.TType.SYMBOL and self.tokenizer.symbol() == "]"):
                raise Exception("Syntax Error; expected ] instead of:" + self.tokenizer.currentToken)
            # index into the arra
            self.out.WriteArithmetic(Config.AType.ADD)
            self.tokenizer.advance()

        if not(self.tokenizer.tokenType() == Config.TType.SYMBOL and self.tokenizer.symbol() == "="):
            raise Exception("Syntax Error; expected = instead of:" + self.tokenizer.currentToken)
        self.out.writePop(Config.SType.POINTER,1)
        self.tokenizer.advance()
        self.CompileExpression()
        self.out.writePop(Config.SType.THAT,0)
        if not(self.tokenizer.tokenType() == Config.TType.SYMBOL and self.tokenizer.symbol() == ";"):
            raise Exception("Syntax Error; expected ; instead of:" + self.tokenizer.currentToken)

        self.tokenizer.advance()


    def CompileDo(self):

        if not(self.tokenizer.tokenType() == Config.TType.KEYWORD and self.tokenizer.symbol() == "do"):
            raise Exception("Syntax Error; expected do instead of:" + self.tokenizer.currentToken)

        self.tokenizer.advance()
        if not(self.tokenizer.tokenType() == Config.TType.IDENTIFIER):
            raise Exception("Syntax Error; expected identifier instead of:" + self.tokenizer.currentToken)
        idt1=self.tokenizer.identifier()
        if not (self.function_sym_table.KindOf(idt1) is None):
            pass
        else:
            pass
        self.tokenizer.advance()
        if self.tokenizer.tokenType() == Config.TType.SYMBOL and self.tokenizer.symbol() == ".":

            self.tokenizer.advance()
            if not(self.tokenizer.tokenType() == Config.TType.IDENTIFIER):
                raise Exception("Syntax Error; expected identifier instead of:" + self.tokenizer.currentToken)
            idt2=self.tokenizer.identifier()
            if not (self.function_sym_table.KindOf(idt2) is None):
                pass
            else:
                pass
            self.tokenizer.advance()
        if not(self.tokenizer.tokenType() == Config.TType.SYMBOL and self.tokenizer.symbol() == "("):
            raise Exception("Syntax Error; expected ( instead of:" + self.tokenizer.currentToken)

        self.tokenizer.advance()
        self.argCount=0
        self.CompileExpressionList()
        if not(self.tokenizer.tokenType() == Config.TType.SYMBOL and self.tokenizer.symbol() == ")"):
            raise Exception("Syntax Error; expected ) instead of:" + self.tokenizer.currentToken)
        self.out.WriteCall(idt1+"."+idt2,self.argCount)
        self.out.writePop(Config.SType.TEMP,0)
        self.tokenizer.advance()
        if not(self.tokenizer.tokenType() == Config.TType.SYMBOL and self.tokenizer.symbol() == ";"):
            raise Exception("Syntax Error; expected ; instead of:" + self.tokenizer.currentToken)

        self.tokenizer.advance()


    def CompileWhile(self):

        if not(self.tokenizer.tokenType() == Config.TType.KEYWORD and self.tokenizer.symbol() == "while"):
            raise Exception("Syntax Error; expected while instead of:" + self.tokenizer.currentToken)

        self.tokenizer.advance()
        if not(self.tokenizer.tokenType() == Config.TType.SYMBOL and self.tokenizer.symbol() == "("):
            raise Exception("Syntax Error; expected ( instead of:" + self.tokenizer.currentToken)

        self.tokenizer.advance()
        self.CompileExpression()
        if not(self.tokenizer.tokenType() == Config.TType.SYMBOL and self.tokenizer.symbol() == ")"):
            raise Exception("Syntax Error; expected ) instead of:" + self.tokenizer.currentToken)

        self.tokenizer.advance()
        if not(self.tokenizer.tokenType() == Config.TType.SYMBOL and self.tokenizer.symbol() == "{"):
            raise Exception("Syntax Error; expected { instead of:" + self.tokenizer.currentToken)

        self.tokenizer.advance()
        self.CompileStatements()
        if not(self.tokenizer.tokenType() == Config.TType.SYMBOL and self.tokenizer.symbol() == "}"):
            raise Exception("Syntax Error; expected } instead of:" + self.tokenizer.currentToken)

        self.tokenizer.advance()


    def CompileIf(self):

        if not(self.tokenizer.tokenType() == Config.TType.KEYWORD and self.tokenizer.symbol() == "if"):
            raise Exception("Syntax Error; expected if instead of:" + self.tokenizer.currentToken)

        self.tokenizer.advance()
        if not(self.tokenizer.tokenType() == Config.TType.SYMBOL and self.tokenizer.symbol() == "("):
            raise Exception("Syntax Error; expected ( instead of:" + self.tokenizer.currentToken)

        self.tokenizer.advance()
        self.CompileExpression()
        if not(self.tokenizer.tokenType() == Config.TType.SYMBOL and self.tokenizer.symbol() == ")"):
            raise Exception("Syntax Error; expected ) instead of:" + self.tokenizer.currentToken)

        self.tokenizer.advance()
        if not(self.tokenizer.tokenType() == Config.TType.SYMBOL and self.tokenizer.symbol() == "{"):
            raise Exception("Syntax Error; expected { instead of:" + self.tokenizer.currentToken)

        self.tokenizer.advance()
        self.CompileStatements()
        if not(self.tokenizer.tokenType() == Config.TType.SYMBOL and self.tokenizer.symbol() == "}"):
            raise Exception("Syntax Error; expected } instead of:" + self.tokenizer.currentToken)

        self.tokenizer.advance()
        if self.tokenizer.tokenType() == Config.TType.KEYWORD and self.tokenizer.symbol() == "else":

            self.tokenizer.advance()
            if not(self.tokenizer.tokenType() == Config.TType.SYMBOL and self.tokenizer.symbol() == "{"):
                raise Exception("Syntax Error; expected { instead of:" + self.tokenizer.currentToken)

            self.tokenizer.advance()
            self.CompileStatements()
            if not(self.tokenizer.tokenType() == Config.TType.SYMBOL and self.tokenizer.symbol() == "}"):
                raise Exception("Syntax Error; expected } instead of:" + self.tokenizer.currentToken)

            self.tokenizer.advance()



    def CompileStatements(self):
        #TMP; only return works

        while True:
            if self.tokenizer.tokenType()==Config.TType.KEYWORD and self.tokenizer.keyword()=="return":
                self.CompileReturn()
            elif self.tokenizer.tokenType()==Config.TType.KEYWORD and self.tokenizer.keyword()=="do":
                self.CompileDo()
            elif self.tokenizer.tokenType()==Config.TType.KEYWORD and self.tokenizer.keyword()=="let":
                self.CompileLet()
            elif self.tokenizer.tokenType()==Config.TType.KEYWORD and self.tokenizer.keyword()=="while":
                self.CompileWhile()
            elif self.tokenizer.tokenType()==Config.TType.KEYWORD and self.tokenizer.keyword()=="if":
                self.CompileIf()
            else:
                break


    def CompileSubroutine(self):

        #initializiing function symbol table and helper variable
        self.isVoid = False
        self.function_sym_table=SymbolTable.SymbolTable()

        if not(self.tokenizer.tokenType() == Config.TType.KEYWORD and self.tokenizer.keyword() in ["constructor","function","method"]):
            raise Exception("Syntax Error; expected \"constructor\",\"function\" or \"method\" or class instead of:" + self.tokenizer.currentToken)
        #identifier
        subroutine_type=self.tokenizer.tokenType()
        self.tokenizer.advance()
        if self.tokenizer.tokenType() == Config.TType.KEYWORD and self.tokenizer.keyword() in ["int","char","boolean"]:
            pass
        elif self.tokenizer.tokenType()== Config.TType.KEYWORD and self.tokenizer.keyword() == "void":
            self.isVoid=True
        elif self.tokenizer.tokenType() == Config.TType.IDENTIFIER:
            pass
        else:
            raise Exception("Syntax Error; expected void, primitive type or class instead of:" + self.tokenizer.currentToken)

        self.tokenizer.advance()
        if not (self.tokenizer.tokenType() == Config.TType.IDENTIFIER):
            raise Exception("Syntax Error; expected identifier instead of:" + self.tokenizer.currentToken)

        tmp_name=self.tokenizer.currentToken

        if self.isVoid:
            self.void_functions.append(self.class_name+"."+tmp_name)

        self.tokenizer.advance()
        if not(self.tokenizer.tokenType() == Config.TType.SYMBOL and self.tokenizer.symbol() == "("):
            raise Exception("Syntax Error; expected ( instead of: " + self.tokenizer.currentToken)

        self.tokenizer.advance()

        self.CompileParameterList()

        if not(self.tokenizer.tokenType() == Config.TType.SYMBOL and self.tokenizer.symbol() == ")"):
            raise Exception("Syntax Error; expected ) instead of: " + self.tokenizer.currentToken)

        self.tokenizer.advance()

        if not(self.tokenizer.tokenType() == Config.TType.SYMBOL and self.tokenizer.symbol() == "{"):
            raise Exception("Syntax Error; expected { instead of: " + self.tokenizer.currentToken)

        self.tokenizer.advance()
        self.varCount=0;
        while self.tokenizer.tokenType() == Config.TType.KEYWORD and self.tokenizer.keyword() == "var":
            self.CompileVarDec()

        if subroutine_type == "method":
            self.varCount=self.varCount+1
            self.out.WriteFunction(self.class_name+"."+tmp_name,self.varCount)
            self.out.writePop("pointer",0)
        elif subroutine_type == "constructor":
            #TODO
            pass
        else:
            self.out.WriteFunction(self.class_name+"."+tmp_name,self.varCount)

        self.CompileStatements()
        if not(self.tokenizer.tokenType() == Config.TType.SYMBOL and self.tokenizer.symbol() == "}"):
            raise Exception("Syntax Error; expected } instead of: " + self.tokenizer.currentToken)
        self.tokenizer.advance()




