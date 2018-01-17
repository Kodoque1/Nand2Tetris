#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      bla
#
# Created:     18/12/2015
# Copyright:   (c) bla 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import unittest
import SymbolTable
import Config

class SymbolTableTest(unittest.TestCase):
    def test_Constructor(self):
        test=SymbolTable.SymbolTable()
        self.assertEqual({},test.table)
        self.assertEqual(0,test.ktable[Config.Kind.FIELD])
        self.assertEqual(0,test.ktable[Config.Kind.ARG])
        self.assertEqual(0,test.ktable[Config.Kind.VAR])
        self.assertEqual(0,test.ktable[Config.Kind.STATIC])

    def test_Define(self):
        test=SymbolTable.SymbolTable()
        test.Define("test","int",Config.Kind.FIELD)
        self.assertEqual(1,test.ktable[Config.Kind.FIELD])
        self.assertTrue("test" in test.table.keys())
        self.assertEqual(["int",Config.Kind.FIELD,1],test.table["test"])

## The rest is trivial, finish later if really needed

if __name__ == '__main__':
    unittest.main()
