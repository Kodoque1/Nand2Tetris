#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      bla
#
# Created:     29/11/2015
# Copyright:   (c) bla 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import unittest
import OutputEngine
import os

class OutputEngineTest(unittest.TestCase):
    def setUp(self):
        self.opt=open("test.txt","w")
        self.oe_test=OutputEngine.OutputEngine(self.opt)

    def test_writeBeginningTag(self):
        self.oe_test.writeBeginningTag("test")
        self.oe_test.output.flush()
        os.fsync(self.oe_test.output)
        g=open("test.txt")
        self.assertEqual(g.readline(),"<test>\n")
        g.close()
        #reset
        self.oe_test.output.seek(0)
        self.oe_test.output.truncate()

    def test_writeEndingTag(self):
        self.oe_test.writeEndingTag("test")
        self.oe_test.output.flush()
        os.fsync(self.oe_test.output)
        g=open("test.txt")
        self.assertEqual(g.readline(),"</test>\n")
        g.close()
        self.oe_test.output.seek(0)
        self.oe_test.output.truncate()

    def test_writeFullTag(self):
        self.oe_test.writeFullTag("test","content")
        self.oe_test.output.flush()
        os.fsync(self.oe_test.output)
        g=open("test.txt")
        self.assertEqual(g.readline(),"<test> content </test>\n")
        g.close()
        self.oe_test.output.seek(0)
        self.oe_test.output.truncate()

    def test_close(self):
        self.oe_test.close()
        self.assertTrue(self.oe_test.output.closed)

    def tearDown(self):
        self.oe_test.close()
        os.remove("test.txt")

if __name__ == '__main__':
    unittest.main()
