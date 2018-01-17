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

import CompilationEngine
import argparse

def main():
    # Parameter Configuration
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-f",dest="file")
    args=parser.parse_args()

    #Object Initialization
    print "Starting Compilation"
    comp=CompilationEngine.CompilationEngine(open(args.file),open(args.file.split(".")[0]+".xml","w"),False)

if __name__ == '__main__':
    main()
