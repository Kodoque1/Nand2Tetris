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


import argparse
import re
import os

#Define for table indexation

TYPE=0
KIND=1
INDEX=2

def enum(**enums):
    return type('Enum', (), enums)

TType=enum(KEYWORD = 1,SYMBOL = 2, INT_CONST = 3, STRING_CONST = 4,IDENTIFIER = 5)

SType=enum(CONST=1,LOCAL=2, POINTER = 3, ARG = 4, STATIC = 5, THIS = 6, THAT = 6, TEMP = 8)

AType=enum(ADD = 1, SUB = 2, NEG = 3, EQ = 4, GT = 5, LT = 6, AND = 7, OR = 8, NOT = 9)

Kind=enum(STATIC = 1, FIELD = 2, ARG = 3, VAR = 4)

list_keyword=["class","constructor","function","method","field","static","var"
            ,"int","char","boolean","void","true","false","null","this","let",
            "do","if","else","while","return"]

list_symbol=["{","}","(",")","[","]",".",",",";","+","-","*","/","&","|","<",">","=","~"]

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
