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

import unittest
import JackTokenizer
import StringIO
import Config

class JackTokenizerTest(unittest.TestCase):

    def test_advance_keyword(self):
        ipt=StringIO.StringIO("while")
        tokenizer=JackTokenizer.JackTokenizer(ipt)
        try:
            tokenizer.advance()
        except Exception as e:
            print str(e)
        self.assertEqual(tokenizer.currentToken,"while")
        self.assertEqual(tokenizer.ttype,Config.TType.KEYWORD)
        self.assertEqual(tokenizer.pos,5)

    def test_advance_symbol(self):
        ipt=StringIO.StringIO("(")
        tokenizer=JackTokenizer.JackTokenizer(ipt)
        try:
            tokenizer.advance()
        except Exception as e:
            print str(e)
        self.assertEqual(tokenizer.currentToken,"(")
        self.assertEqual(tokenizer.ttype,Config.TType.SYMBOL)
        self.assertEqual(tokenizer.pos,1)

    def test_advance_integerConstant(self):
        ipt=StringIO.StringIO("180")
        tokenizer=JackTokenizer.JackTokenizer(ipt)
        try:
            tokenizer.advance()
        except Exception as e:
            print str(e)
        self.assertEqual(tokenizer.currentToken,"180")
        self.assertEqual(tokenizer.ttype,Config.TType.INT_CONST)
        self.assertEqual(tokenizer.pos,3)

    def test_advance_stringConstant(self):
        ipt=StringIO.StringIO("\"test\"")
        tokenizer=JackTokenizer.JackTokenizer(ipt)
        try:
            tokenizer.advance()
        except Exception as e:
            print str(e)
        self.assertEqual(tokenizer.currentToken,"\"test\"")
        self.assertEqual(tokenizer.ttype,Config.TType.STRING_CONST)
        self.assertEqual(tokenizer.pos,6)

    def test_advance_stringConstant(self):
        ipt=StringIO.StringIO("\"test\"")
        tokenizer=JackTokenizer.JackTokenizer(ipt)
        try:
            tokenizer.advance()
        except Exception as e:
            print str(e)
        self.assertEqual(tokenizer.currentToken,"\"test\"")
        self.assertEqual(tokenizer.ttype,Config.TType.STRING_CONST)
        self.assertEqual(tokenizer.pos,6)


    def test_advance_identifier(self):
        ipt=StringIO.StringIO("foobar")
        tokenizer=JackTokenizer.JackTokenizer(ipt)
        try:
            tokenizer.advance()
        except Exception as e:
            print str(e)
        self.assertEqual(tokenizer.currentToken,"foobar")
        self.assertEqual(tokenizer.ttype,Config.TType.IDENTIFIER)
        self.assertEqual(tokenizer.pos,6)

    def test_advance_multi_token(self):
        ipt=StringIO.StringIO("""while (     foobar)// test\n
        /** \n
        test\n
        */
        /**\n
        */
        /*ignore*/var=3*\"test\"\n/**   \n */   """)
        tokenizer=JackTokenizer.JackTokenizer(ipt)
        tmp=[]
        while tokenizer.hasMoreTokens():
            tokenizer.advance()
            if tokenizer.ttype:
                tmp.append((tokenizer.currentToken,tokenizer.ttype))

        good_result=[("while",Config.TType.KEYWORD)
        ,("(",Config.TType.SYMBOL)
        ,("foobar",Config.TType.IDENTIFIER)
        ,(")",Config.TType.SYMBOL)
        ,("var",Config.TType.KEYWORD)
        ,("=",Config.TType.SYMBOL)
        ,("3",Config.TType.INT_CONST)
        ,("*",Config.TType.SYMBOL)
        ,("\"test\"",Config.TType.STRING_CONST)]

        self.assertEqual(tmp,good_result)

    def test_tokentype(self):
        ipt=StringIO.StringIO("while")
        tokenizer=JackTokenizer.JackTokenizer(ipt)
        tokenizer.advance()
        self.assertEqual(tokenizer.tokenType(),Config.TType.KEYWORD)

    def test_hasMoreTokens_notEmpty(self):
        ipt=StringIO.StringIO("while")
        tokenizer=JackTokenizer.JackTokenizer(ipt)
        self.assertTrue(tokenizer.hasMoreTokens())

    def test_hasMoreTokens_Empty(self):
        ipt=StringIO.StringIO("")
        tokenizer=JackTokenizer.JackTokenizer(ipt)
        self.assertFalse(tokenizer.hasMoreTokens())

    def test_symbol(self):
        ipt=StringIO.StringIO("(")
        tokenizer=JackTokenizer.JackTokenizer(ipt)
        tokenizer.advance()
        self.assertEquals(tokenizer.symbol(),"(")

    def test_intVal(self):
        ipt=StringIO.StringIO("18")
        tokenizer=JackTokenizer.JackTokenizer(ipt)
        tokenizer.advance()
        self.assertEquals(tokenizer.intVal(),18)

    def test_stringVal(self):
        ipt=StringIO.StringIO("\"18\"")
        tokenizer=JackTokenizer.JackTokenizer(ipt)
        tokenizer.advance()
        self.assertEquals(tokenizer.stringVal(),"18")

if __name__ == '__main__':
    unittest.main()

