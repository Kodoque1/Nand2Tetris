#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      bla
#
# Created:     01/12/2015
# Copyright:   (c) bla 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import Config
import re
import cgi

kw_regexp="("+"|".join([kw for kw in Config.list_keyword])+")(?![a-zA-Z0-9_])"
sym_regexp="("+"|".join(map(re.escape,Config.list_symbol))+")"
int_const_regexp="([0-9]+)"
string_const_regexp="(\".*\")"
identifier_regexp="([a-zA-Z_][a-zA-Z0-9_]*)"
comment_regexp="(?:(?:/\*(?:.|[\r\n])*?\*/)|(?:/\*.*\*/)|(?://[^\n]*)+\n)"
whitespace_regexp="(?:\s+)"

regexp_string=comment_regexp + "|" +  kw_regexp+"|"+sym_regexp+"|"+int_const_regexp+"|"+string_const_regexp+"|"+identifier_regexp+"|"+whitespace_regexp

class JackTokenizer:
    def __init__(self,f_input):
        self.input_string=f_input.read()
        self.scan=re.compile(regexp_string)
        self.currentToken=""
        self.ttype=None
        self.pos=0

    def advance(self):
        m=self.scan.match(self.input_string,self.pos)
        if m:
            self.pos=m.end()
            self.ttype=m.lastindex
            if (m.lastindex is None):
                if self.hasMoreTokens():
                    self.advance()
            else:
                self.currentToken=m.group(m.lastindex) # Return string
        else:
            raise Exception("Unrecognized Tokens: " + re.escape(self.input_string[self.pos:self.pos+10]) + " ...")

    def keyword(self):
        return self.currentToken

    def symbol(self):
        return self.currentToken

    def identifier(self):
        return self.currentToken

    def intVal(self):
        return int(self.currentToken)

    def stringVal(self):
        return self.currentToken[1:-1]

    def hasMoreTokens(self):
        return len(self.input_string)>self.pos

    def tokenType(self):
        return self.ttype



