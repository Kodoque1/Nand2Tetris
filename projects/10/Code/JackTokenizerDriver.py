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

import JackTokenizer
import OutputEngine
import Config
import cgi
import argparse

def main():
    # Parameter Configuration
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-f",dest="file")
    args=parser.parse_args()

    #Object Initialization
    tokenizer=JackTokenizer.JackTokenizer(open(args.file))
    output=OutputEngine.OutputEngine(args.file.split(".")[0]+".xml")

    # Produce tokenList
    output.writeBeginningTag("tokens")
    while tokenizer.hasMoreTokens():
        tokenizer.advance()
        if tokenizer.tokenType() == Config.TType.KEYWORD:
            output.writeFullTag("keyword",tokenizer.keyword())
        elif tokenizer.tokenType() == Config.TType.SYMBOL:
            output.writeFullTag("symbol",cgi.escape(tokenizer.symbol()))
        elif tokenizer.tokenType() == Config.TType.INT_CONST:
            output.writeFullTag("integerConstant",str(tokenizer.intVal()))
        elif tokenizer.tokenType() == Config.TType.STRING_CONST:
            output.writeFullTag("stringConstant",tokenizer.stringVal())
        elif tokenizer.tokenType() == Config.TType.IDENTIFIER:
            output.writeFullTag("identifier",tokenizer.identifier())
    output.writeEndingTag("tokens")

    output.close()

if __name__ == '__main__':
    main()
