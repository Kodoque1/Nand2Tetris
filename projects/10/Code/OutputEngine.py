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

import cgi

class OutputEngine:
    def __init__(self,output):
        self.output=output

    def writeBeginningTag(self,tagname):
        self.output.write("<"+tagname+">" + "\n")

    def writeEndingTag(self,tagname):
        self.output.write("</"+tagname+">"+"\n")

    # Because of eacute, we escape the cgi content
    def writeFullTag(self,tagname,content):
        self.output.write("<"+tagname+"> "+cgi.escape(content)+" </"+tagname+">"+"\n")

    def close(self):
        self.output.close()