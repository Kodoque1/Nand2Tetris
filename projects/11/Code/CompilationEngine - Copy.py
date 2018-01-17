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

class CompilationEngine():

    def __init__(self,finput,foutput,debugmode):
        self.out=OutputEngine.OutputEngine(foutput)
        self.tokenizer=JackTokenizer.JackTokenizer(finput)

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
        self.out.writeBeginningTag("class")
        if not (self.tokenizer.tokenType() == Config.TType.KEYWORD and self.tokenizer.keyword() == "class"):
            raise Exception("Syntax Error; expected \"class\" instead of:" + self.tokenizer.currentToken)
        self.out.writeFullTag("keyword","class")
        self.tokenizer.advance()
        if not(self.tokenizer.tokenType() == Config.TType.IDENTIFIER):
            raise Exception("Syntax Error; expected identifier instead of:" + self.tokenizer.currentToken)
        self.out.writeFullTag("identifier category=class",self.tokenizer.identifier())
        self.tokenizer.advance()
        if not(self.tokenizer.tokenType() == Config.TType.SYMBOL and self.tokenizer.keyword() == "{"):
            raise Exception("Syntax Error; expected \"{\" instead of:" + self.tokenizer.currentToken)
        self.out.writeFullTag("symbol",self.tokenizer.symbol())
        self.tokenizer.advance()
        while self.tokenizer.tokenType() == Config.TType.KEYWORD and self.tokenizer.keyword() in ["static","field"]:
            self.CompileClassVarDec()
        while self.tokenizer.tokenType() == Config.TType.KEYWORD and self.tokenizer.keyword() in ["constructor","function","method"]:
            self.CompileSubroutine()
        if not(self.tokenizer.tokenType() == Config.TType.SYMBOL and self.tokenizer.keyword() == "}"):
            raise Exception("Syntax Error; expected \"}\" instead of:" + self.tokenizer.currentToken)
        self.out.writeFullTag("symbol",self.tokenizer.symbol())
        self.out.writeEndingTag("class")

    def CompileClassVarDec(self):
        JackType=""
        Kind=""

        self.out.writeBeginningTag("classVarDec")
        if not (self.tokenizer.tokenType() == Config.TType.KEYWORD and self.tokenizer.keyword() in ["static","field"]):
            raise Exception("Syntax Error; expected \"static\" or \"field\" instead of:" + self.tokenizer.currentToken)
        self.out.writeFullTag("keyword",self.tokenizer.keyword())
        Kind=self.tokenizer.keyword()
        self.tokenizer.advance()
        if self.tokenizer.tokenType() == Config.TType.KEYWORD and self.tokenizer.keyword() in ["int","char","boolean"]:
            self.out.writeFullTag("keyword",self.tokenizer.keyword())
            JackType=self.tokenizer.keyword()
        elif self.tokenizer.tokenType() == Config.TType.IDENTIFIER:
            self.out.writeFullTag("identifier",self.tokenizer.identifier())
            JackType=self.tokenizer.identifier()
        else:
            raise Exception("Syntax Error; expected primitive type or class instead of:" + self.tokenizer.currentToken)
        self.tokenizer.advance()
        if not (self.tokenizer.tokenType() == Config.TType.IDENTIFIER):
            raise Exception("Syntax Error; expected identifier instead of:" + self.tokenizer.currentToken)
        self.out.writeFullTag("identifier status=defined type="+JackType+" kind="+Kind,self.tokenizer.identifier())
        class_sym_table.Define(self.tokenizer.identifier(),JackType,Kind)
        self.tokenizer.advance()
        while self.tokenizer.tokenType() == Config.TType.SYMBOL and self.tokenizer.symbol() == ",":
            self.out.writeFullTag("symbol",self.tokenizer.symbol())
            self.tokenizer.advance()
            if not (self.tokenizer.tokenType() == Config.TType.IDENTIFIER):
                raise Exception("Syntax Error; expected identifier instead of:" + self.tokenizer.currentToken)
            self.out.writeFullTag("identifier status=defined type="+JackType+" kind="+Kind,self.tokenizer.identifier())
            class_sym_table.Define(self.tokenizer.identifier(),JackType,Kind)
            self.tokenizer.advance()
        if not(self.tokenizer.tokenType() == Config.TType.SYMBOL and self.tokenizer.symbol() == ";"):
            raise Exception("Syntax Error; expected \";\" instead of: " + self.tokenizer.currentToken)
        self.out.writeFullTag("symbol",self.tokenizer.symbol())
        self.tokenizer.advance()
        self.out.writeEndingTag("classVarDec")


    def CompileVarDec(self):

        JackType=""

        self.out.writeBeginningTag("varDec")
        if not(self.tokenizer.tokenType() == Config.TType.KEYWORD and self.tokenizer.keyword() == "var"):
            raise Exception("Syntax Error; expected var instead of: " + self.tokenizer.currentToken)
        self.out.writeFullTag("keyword",self.tokenizer.keyword())
        self.tokenizer.advance();
        if self.tokenizer.tokenType() == Config.TType.KEYWORD and self.tokenizer.keyword() in ["int","char","boolean"]:
            self.out.writeFullTag("keyword",self.tokenizer.keyword())
            JackType=self.tokenizer.keyword()
        elif self.tokenizer.tokenType() == Config.TType.IDENTIFIER:
            self.out.writeFullTag("identifier",self.tokenizer.identifier())
            JackType=self.tokenizer.identifier()
        else:
            raise Exception("Syntax Error; expected primitive type or class instead of:" + self.tokenizer.currentToken)
        self.tokenizer.advance()
        if not (self.tokenizer.tokenType() == Config.TType.IDENTIFIER):
            raise Exception("Syntax Error; expected identifier instead of:" + self.tokenizer.currentToken)
        self.out.writeFullTag("identifier status=defined type="+JackType+" kind=VAR",self.tokenizer.identifier())
        function_sym_table.Define(self.tokenizer.identifier(),JackType,Config.Kind.VAR)
        self.tokenizer.advance()
        while self.tokenizer.tokenType() == Config.TType.SYMBOL and self.tokenizer.symbol() == ",":
            self.out.writeFullTag("symbol",self.tokenizer.symbol())
            self.tokenizer.advance()
            if not (self.tokenizer.tokenType() == Config.TType.IDENTIFIER):
                raise Exception("Syntax Error; expected identifier instead of:" + self.tokenizer.currentToken)
            self.out.writeFullTag("identifier status=defined type="+JackType+" kind=VAR",self.tokenizer.identifier())
            function_sym_table.Define(self.tokenizer.identifier(),JackType,Config.Kind.VAR)
            self.tokenizer.advance()
        if not(self.tokenizer.tokenType() == Config.TType.SYMBOL and self.tokenizer.symbol() == ";"):
            raise Exception("Syntax Error; expected \";\" instead of: " + self.tokenizer.currentToken)
        self.out.writeFullTag("symbol",self.tokenizer.symbol())
        self.tokenizer.advance()
        self.out.writeEndingTag("varDec")

    def CompileParameterList(self):
        JackType=""
        self.out.writeBeginningTag("parameterList")
        if not(self.tokenizer.tokenType() == Config.TType.SYMBOL and self.tokenizer.symbol() == ")"):
            if self.tokenizer.tokenType() == Config.TType.KEYWORD and self.tokenizer.keyword() in ["int","char","boolean"]:
                self.out.writeFullTag("keyword",self.tokenizer.keyword())
                JackType=self.tokenizer.keyword()
            elif self.tokenizer.tokenType() == Config.TType.IDENTIFIER:
                self.out.writeFullTag("identifier",self.tokenizer.identifier())
                JackType=self.tokenizer.identifier()
            else:
                raise Exception("Syntax Error; expected primitive type or class instead of:" + self.tokenizer.currentToken)
            self.tokenizer.advance()
            if not (self.tokenizer.tokenType() == Config.TType.IDENTIFIER):
                raise Exception("Syntax Error; expected identifier instead of:" + self.tokenizer.currentToken)
            self.out.writeFullTag("identifier status=defined type="+JackType+" kind=Arg",self.tokenizer.identifier())
            sym_table.Define(self.tokenizer.identifier(),JackType,Config.Kind.Arg)
            self.tokenizer.advance()
            while self.tokenizer.tokenType() == Config.TType.SYMBOL and self.tokenizer.symbol() == ",":
                self.out.writeFullTag("symbol",self.tokenizer.symbol())
                self.tokenizer.advance()
                if self.tokenizer.tokenType() == Config.TType.KEYWORD and self.tokenizer.keyword() in ["int","char","boolean"]:
                    self.out.writeFullTag("keyword",self.tokenizer.keyword())
                    JackType=self.tokenizer.keyword()
                elif self.tokenizer.tokenType() == Config.TType.IDENTIFIER:
                    self.out.writeFullTag("identifier",self.tokenizer.identifier())
                    JackType=self.tokenizer.identifier()
                else:
                    raise Exception("Syntax Error; expected primitive type or class instead of:" + self.tokenizer.currentToken)
                self.tokenizer.advance()
                if not (self.tokenizer.tokenType() == Config.TType.IDENTIFIER):
                    raise Exception("Syntax Error; expected identifier instead of:" + self.tokenizer.currentToken)
                self.out.writeFullTag("identifier status=defined type="+JackType+" kind=Arg",self.tokenizer.identifier())
                sym_table.Define(self.tokenizer.identifier(),JackType,Config.Kind.Arg)
                self.tokenizer.advance()
        self.out.writeEndingTag("parameterList")

    def CompileExpression(self):
        self.out.writeBeginningTag("expression")
        self.CompileTerm()
        while self.tokenizer.tokenType() == Config.TType.SYMBOL and self.tokenizer.symbol() in Config.list_op:
            self.out.writeFullTag("symbol",self.tokenizer.symbol())
            self.tokenizer.advance()
            self.CompileTerm()
        self.out.writeEndingTag("expression")

    def CompileTerm(self):
        self.out.writeBeginningTag("term")
        if self.tokenizer.tokenType() == Config.TType.STRING_CONST:
            self.out.writeFullTag("stringConstant",self.tokenizer.stringVal())
            self.tokenizer.advance()
        elif self.tokenizer.tokenType() == Config.TType.INT_CONST:
            self.out.writeFullTag("integerConstant",str(self.tokenizer.intVal()))
            self.tokenizer.advance()
        elif self.tokenizer.tokenType() == Config.TType.KEYWORD:
            self.out.writeFullTag("keyword",self.tokenizer.symbol())
            self.tokenizer.advance()
        elif self.tokenizer.tokenType() == Config.TType.SYMBOL and self.tokenizer.symbol() == "(":
            self.out.writeFullTag("symbol",self.tokenizer.symbol())
            self.tokenizer.advance()
            self.CompileExpression()
            if not(self.tokenizer.tokenType() == Config.TType.SYMBOL and self.tokenizer.symbol() == ")"):
                raise Exception("Syntax Error; expected ) instead of:" + self.tokenizer.currentToken)
            self.out.writeFullTag("symbol",self.tokenizer.symbol())
            self.tokenizer.advance()
        elif self.tokenizer.tokenType() == Config.TType.SYMBOL and self.tokenizer.symbol() in Config.list_unary:
            self.out.writeFullTag("symbol",self.tokenizer.symbol())
            self.tokenizer.advance()
            self.CompileTerm()
        elif self.tokenizer.tokenType() == Config.TType.IDENTIFIER:
            idt=self.tokenizer.identifier()
            if not (sym_table.KindOf(idt) is None):
                self.out.writeFullTag("identifier status=used type="+sym_table.TypeOf(idt)+" kind="+sym_table.KindOf(idt),self.tokenizer.identifier())
            else:
                self.out.writeFullTag("identifier",idt)
            self.tokenizer.advance()
            if self.tokenizer.tokenType() == Config.TType.SYMBOL and self.tokenizer.symbol() in [".","("]:
                if self.tokenizer.tokenType() == Config.TType.SYMBOL and self.tokenizer.symbol() == ".":
                    self.out.writeFullTag("symbol",self.tokenizer.symbol())
                    self.tokenizer.advance()
                    if not(self.tokenizer.tokenType() == Config.TType.IDENTIFIER):
                        raise Exception("Syntax Error; expected identifier instead of:" + self.tokenizer.currentToken)
                    self.out.writeFullTag("identifier",self.tokenizer.identifier())
                    self.tokenizer.advance()
                if not(self.tokenizer.tokenType() == Config.TType.SYMBOL and self.tokenizer.symbol() == "("):
                    raise Exception("Syntax Error; expected ( instead of:" + self.tokenizer.currentToken)
                self.out.writeFullTag("symbol",self.tokenizer.symbol())
                self.tokenizer.advance()
                self.CompileExpressionList()
                if not(self.tokenizer.tokenType() == Config.TType.SYMBOL and self.tokenizer.symbol() == ")"):
                    raise Exception("Syntax Error; expected ) instead of:" + self.tokenizer.currentToken)
                self.out.writeFullTag("symbol",self.tokenizer.symbol())
                self.tokenizer.advance()
            elif self.tokenizer.tokenType() == Config.TType.SYMBOL and self.tokenizer.symbol() == "[":
                self.out.writeFullTag("symbol",self.tokenizer.symbol())
                self.tokenizer.advance()
                self.CompileExpression()
                if not(self.tokenizer.tokenType() == Config.TType.SYMBOL and self.tokenizer.symbol() == "]"):
                    raise Exception("Syntax Error; expected ) instead of:" + self.tokenizer.currentToken)
                self.out.writeFullTag("symbol",self.tokenizer.symbol())
                self.tokenizer.advance()
        else:
            raise Exception("Syntax Error; expected term instead of:" + self.tokenizer.currentToken)
        self.out.writeEndingTag("term")

    def CompileExpressionList(self):
        self.out.writeBeginningTag("expressionList")
        if not(self.tokenizer.tokenType() == Config.TType.SYMBOL and self.tokenizer.symbol() == ")"):
            self.CompileExpression()
            while self.tokenizer.tokenType() == Config.TType.SYMBOL and self.tokenizer.symbol() == ",":
                self.out.writeFullTag("symbol",self.tokenizer.symbol())
                self.tokenizer.advance()
                self.CompileExpression()
        self.out.writeEndingTag("expressionList")

    def CompileReturn(self):
        self.out.writeBeginningTag("returnStatement")
        if not(self.tokenizer.tokenType() == Config.TType.KEYWORD and self.tokenizer.keyword() == "return"):
            raise Exception("Syntax Error; expected \"return\" instead of:" + self.tokenizer.currentToken)
        self.out.writeFullTag("keyword","return")
        self.tokenizer.advance()
        if not(self.tokenizer.tokenType() == Config.TType.SYMBOL and self.tokenizer.symbol() == ";"):
            self.CompileExpression()
        if not(self.tokenizer.tokenType() == Config.TType.SYMBOL and self.tokenizer.symbol() == ";"):
            raise Exception("Syntax Error; expected \";\" instead of:" + self.tokenizer.currentToken)
        self.out.writeFullTag("symbol",";")
        self.tokenizer.advance()
        self.out.writeEndingTag("returnStatement")

    def CompileLet(self):
        self.out.writeBeginningTag("letStatement")
        if not(self.tokenizer.tokenType() == Config.TType.KEYWORD and self.tokenizer.symbol() == "let"):
            raise Exception("Syntax Error; expected let instead of:" + self.tokenizer.currentToken)
        self.out.writeFullTag("keyword",self.tokenizer.keyword())
        self.tokenizer.advance()
        if not(self.tokenizer.tokenType() == Config.TType.IDENTIFIER):
            raise Exception("Syntax Error; expected identifier instead of:" + self.tokenizer.currentToken)
        idt=self.tokenizer.identifier()
        if not (sym_table.KindOf(idt) is None):
                self.out.writeFullTag("identifier status=used type="+sym_table.TypeOf(idt)+" kind="+sym_table.KindOf(idt),self.tokenizer.identifier())
        else:
            self.out.writeFullTag("identifier",idt)
        self.out.writeFullTag("identifier",self.tokenizer.identifier())
        self.tokenizer.advance()
        if self.tokenizer.tokenType() == Config.TType.SYMBOL and self.tokenizer.symbol() == "[":
            self.out.writeFullTag("symbol",self.tokenizer.symbol())
            self.tokenizer.advance()
            self.CompileExpression()
            if not(self.tokenizer.tokenType() == Config.TType.SYMBOL and self.tokenizer.symbol() == "]"):
                raise Exception("Syntax Error; expected ] instead of:" + self.tokenizer.currentToken)
            self.out.writeFullTag("symbol",self.tokenizer.symbol())
            self.tokenizer.advance()
        if not(self.tokenizer.tokenType() == Config.TType.SYMBOL and self.tokenizer.symbol() == "="):
            raise Exception("Syntax Error; expected = instead of:" + self.tokenizer.currentToken)
        self.out.writeFullTag("symbol",self.tokenizer.symbol())
        self.tokenizer.advance()
        self.CompileExpression()
        if not(self.tokenizer.tokenType() == Config.TType.SYMBOL and self.tokenizer.symbol() == ";"):
            raise Exception("Syntax Error; expected ; instead of:" + self.tokenizer.currentToken)
        self.out.writeFullTag("symbol",self.tokenizer.symbol())
        self.tokenizer.advance()
        self.out.writeEndingTag("letStatement")

    def CompileDo(self):
        self.out.writeBeginningTag("doStatement")
        if not(self.tokenizer.tokenType() == Config.TType.KEYWORD and self.tokenizer.symbol() == "do"):
            raise Exception("Syntax Error; expected do instead of:" + self.tokenizer.currentToken)
        self.out.writeFullTag("keyword",self.tokenizer.keyword())
        self.tokenizer.advance()
        if not(self.tokenizer.tokenType() == Config.TType.IDENTIFIER):
            raise Exception("Syntax Error; expected identifier instead of:" + self.tokenizer.currentToken)
        idt=self.tokenizer.identifier()
        if not (sym_table.KindOf(idt) is None):
                self.out.writeFullTag("identifier status=used type="+sym_table.TypeOf(idt)+" kind="+sym_table.KindOf(idt),self.tokenizer.identifier())
        else:
            self.out.writeFullTag("identifier",idt)
        self.tokenizer.advance()
        if self.tokenizer.tokenType() == Config.TType.SYMBOL and self.tokenizer.symbol() == ".":
            self.out.writeFullTag("symbol",self.tokenizer.symbol())
            self.tokenizer.advance()
            if not(self.tokenizer.tokenType() == Config.TType.IDENTIFIER):
                raise Exception("Syntax Error; expected identifier instead of:" + self.tokenizer.currentToken)
            self.out.writeFullTag("identifier",self.tokenizer.identifier())
            self.tokenizer.advance()
        if not(self.tokenizer.tokenType() == Config.TType.SYMBOL and self.tokenizer.symbol() == "("):
            raise Exception("Syntax Error; expected ( instead of:" + self.tokenizer.currentToken)
        self.out.writeFullTag("symbol",self.tokenizer.symbol())
        self.tokenizer.advance()
        self.CompileExpressionList()
        if not(self.tokenizer.tokenType() == Config.TType.SYMBOL and self.tokenizer.symbol() == ")"):
            raise Exception("Syntax Error; expected ) instead of:" + self.tokenizer.currentToken)
        self.out.writeFullTag("symbol",self.tokenizer.symbol())
        self.tokenizer.advance()
        if not(self.tokenizer.tokenType() == Config.TType.SYMBOL and self.tokenizer.symbol() == ";"):
            raise Exception("Syntax Error; expected ; instead of:" + self.tokenizer.currentToken)
        self.out.writeFullTag("symbol",self.tokenizer.symbol())
        self.tokenizer.advance()
        self.out.writeEndingTag("doStatement")

    def CompileWhile(self):
        self.out.writeBeginningTag("whileStatement")
        if not(self.tokenizer.tokenType() == Config.TType.KEYWORD and self.tokenizer.symbol() == "while"):
            raise Exception("Syntax Error; expected while instead of:" + self.tokenizer.currentToken)
        self.out.writeFullTag("keyword",self.tokenizer.keyword())
        self.tokenizer.advance()
        if not(self.tokenizer.tokenType() == Config.TType.SYMBOL and self.tokenizer.symbol() == "("):
            raise Exception("Syntax Error; expected ( instead of:" + self.tokenizer.currentToken)
        self.out.writeFullTag("symbol",self.tokenizer.symbol())
        self.tokenizer.advance()
        self.CompileExpression()
        if not(self.tokenizer.tokenType() == Config.TType.SYMBOL and self.tokenizer.symbol() == ")"):
            raise Exception("Syntax Error; expected ) instead of:" + self.tokenizer.currentToken)
        self.out.writeFullTag("symbol",self.tokenizer.symbol())
        self.tokenizer.advance()
        if not(self.tokenizer.tokenType() == Config.TType.SYMBOL and self.tokenizer.symbol() == "{"):
            raise Exception("Syntax Error; expected { instead of:" + self.tokenizer.currentToken)
        self.out.writeFullTag("symbol",self.tokenizer.symbol())
        self.tokenizer.advance()
        self.CompileStatements()
        if not(self.tokenizer.tokenType() == Config.TType.SYMBOL and self.tokenizer.symbol() == "}"):
            raise Exception("Syntax Error; expected } instead of:" + self.tokenizer.currentToken)
        self.out.writeFullTag("symbol",self.tokenizer.symbol())
        self.tokenizer.advance()
        self.out.writeEndingTag("whileStatement")

    def CompileIf(self):
        self.out.writeBeginningTag("ifStatement")
        if not(self.tokenizer.tokenType() == Config.TType.KEYWORD and self.tokenizer.symbol() == "if"):
            raise Exception("Syntax Error; expected if instead of:" + self.tokenizer.currentToken)
        self.out.writeFullTag("keyword",self.tokenizer.keyword())
        self.tokenizer.advance()
        if not(self.tokenizer.tokenType() == Config.TType.SYMBOL and self.tokenizer.symbol() == "("):
            raise Exception("Syntax Error; expected ( instead of:" + self.tokenizer.currentToken)
        self.out.writeFullTag("symbol",self.tokenizer.symbol())
        self.tokenizer.advance()
        self.CompileExpression()
        if not(self.tokenizer.tokenType() == Config.TType.SYMBOL and self.tokenizer.symbol() == ")"):
            raise Exception("Syntax Error; expected ) instead of:" + self.tokenizer.currentToken)
        self.out.writeFullTag("symbol",self.tokenizer.symbol())
        self.tokenizer.advance()
        if not(self.tokenizer.tokenType() == Config.TType.SYMBOL and self.tokenizer.symbol() == "{"):
            raise Exception("Syntax Error; expected { instead of:" + self.tokenizer.currentToken)
        self.out.writeFullTag("symbol",self.tokenizer.symbol())
        self.tokenizer.advance()
        self.CompileStatements()
        if not(self.tokenizer.tokenType() == Config.TType.SYMBOL and self.tokenizer.symbol() == "}"):
            raise Exception("Syntax Error; expected } instead of:" + self.tokenizer.currentToken)
        self.out.writeFullTag("symbol",self.tokenizer.symbol())
        self.tokenizer.advance()
        if self.tokenizer.tokenType() == Config.TType.KEYWORD and self.tokenizer.symbol() == "else":
            self.out.writeFullTag("keyword",self.tokenizer.keyword())
            self.tokenizer.advance()
            if not(self.tokenizer.tokenType() == Config.TType.SYMBOL and self.tokenizer.symbol() == "{"):
                raise Exception("Syntax Error; expected { instead of:" + self.tokenizer.currentToken)
            self.out.writeFullTag("symbol",self.tokenizer.symbol())
            self.tokenizer.advance()
            self.CompileStatements()
            if not(self.tokenizer.tokenType() == Config.TType.SYMBOL and self.tokenizer.symbol() == "}"):
                raise Exception("Syntax Error; expected } instead of:" + self.tokenizer.currentToken)
            self.out.writeFullTag("symbol",self.tokenizer.symbol())
            self.tokenizer.advance()
        self.out.writeEndingTag("ifStatement")


    def CompileStatements(self):
        #TMP; only return works
        self.out.writeBeginningTag("statements")
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
        self.out.writeEndingTag("statements")

    def CompileSubroutine(self):
        self.out.writeBeginningTag("subroutineDec")
        if not(self.tokenizer.tokenType() == Config.TType.KEYWORD and self.tokenizer.keyword() in ["constructor","function","method"]):
            raise Exception("Syntax Error; expected \"constructor\",\"function\" or \"method\" or class instead of:" + self.tokenizer.currentToken)
        #identifier
        self.out.writeFullTag("keyword",self.tokenizer.keyword())
        self.tokenizer.advance()
        if self.tokenizer.tokenType() == Config.TType.KEYWORD and self.tokenizer.keyword() in ["int","void","char","boolean"]:
            self.out.writeFullTag("keyword",self.tokenizer.keyword())
        elif self.tokenizer.tokenType() == Config.TType.IDENTIFIER:
            self.out.writeFullTag("identifier",self.tokenizer.identifier())
        else:
            raise Exception("Syntax Error; expected void, primitive type or class instead of:" + self.tokenizer.currentToken)
        self.tokenizer.advance()
        if not (self.tokenizer.tokenType() == Config.TType.IDENTIFIER):
            raise Exception("Syntax Error; expected identifier instead of:" + self.tokenizer.currentToken)
        self.out.writeFullTag("identifier",self.tokenizer.identifier())
        self.tokenizer.advance()
        if not(self.tokenizer.tokenType() == Config.TType.SYMBOL and self.tokenizer.symbol() == "("):
            raise Exception("Syntax Error; expected ( instead of: " + self.tokenizer.currentToken)
        self.out.writeFullTag("symbol",self.tokenizer.symbol())
        self.tokenizer.advance()
        self.CompileParameterList()
        if not(self.tokenizer.tokenType() == Config.TType.SYMBOL and self.tokenizer.symbol() == ")"):
            raise Exception("Syntax Error; expected ) instead of: " + self.tokenizer.currentToken)
        self.out.writeFullTag("symbol",self.tokenizer.symbol())
        self.tokenizer.advance()
        self.out.writeBeginningTag("subroutineBody")
        if not(self.tokenizer.tokenType() == Config.TType.SYMBOL and self.tokenizer.symbol() == "{"):
            raise Exception("Syntax Error; expected { instead of: " + self.tokenizer.currentToken)
        self.out.writeFullTag("symbol",self.tokenizer.symbol())
        self.tokenizer.advance()
        while self.tokenizer.tokenType() == Config.TType.KEYWORD and self.tokenizer.keyword() == "var":
            self.CompileVarDec()
        self.CompileStatements()
        if not(self.tokenizer.tokenType() == Config.TType.SYMBOL and self.tokenizer.symbol() == "}"):
            raise Exception("Syntax Error; expected } instead of: " + self.tokenizer.currentToken)
        self.out.writeFullTag("symbol",self.tokenizer.symbol())
        self.tokenizer.advance()
        self.out.writeEndingTag("subroutineBody")
        self.out.writeEndingTag("subroutineDec")



