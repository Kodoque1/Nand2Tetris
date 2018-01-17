import argparse
import os

commandType = {"add":"C_ARITHMETIC",
"sub":"C_ARITHMETIC",
"neg":"C_ARITHMETIC",
"eq":"C_ARITHMETIC",
"gt":"C_ARITHMETIC",
"lt":"C_ARITHMETIC",
"and":"C_ARITHMETIC",
"or":"C_ARITHMETIC",
"not":"C_ARITHMETIC",
"push":"C_PUSH",
"pop":"C_POP",
"label":"C_LABEL",
"goto":"C_GOTO",
"if-goto":"C_IF",
"function":"C_FUNCTION",
"call":"C_CALL",
"return":"C_RETURN"
}

segment_mapping = {
"local":"LCL",
"argument":"ARG",
"this":"THIS",
"that":"THAT"}
two_arg_command = ["C_PUSH","C_POP","C_CALL","C_FUNCTION"]

class Parser:
    def __init__(self,name):
        f = open(name)
        self.istream = filter(lambda x : not (x=="" or x[0:2]=="//"),map(str.strip,f.readlines()))

    def hasMoreCommands(self):
        return len(self.istream) > 0

    def advance(self):
        # IN : There are is still commands
        # OUT : current command gets updated
        if(self.hasMoreCommands()):
            self.currentCommand = self.istream.pop(0)

    def commandType(self):
        tmp = self.currentCommand.split()
        return commandType[tmp[0]]

    def arg1(self):
        if self.commandType()!="C_RETURN":
            if self.commandType()=="C_ARITHMETIC":
                return self.currentCommand
            else:
                return self.currentCommand.split()[1]

    def arg2(self):
        if self.commandType() in two_arg_command:
            return self.currentCommand.split()[2]

class CodeWriter:
    def __init__(self,name):
        self.output=open(name,"w")
        #self.writeInit()
        self.bool_op=0
        self.call_cnt=0
        self.context=""

    def writeInit():
        tmp="@256\n"
        tmp+="D=A\n"
        tmp+="@0"
        tmp+="M=D\n"
        self.output.write(tmp)

    def writeLabel(name):
        self.output.write("("+name+")\n")

    def writeGoto(name):
        tmp="@"+name+"\n"
        tmp+="0;JMP\n"
        self.output.write(tmp)

    def writeIf(name):
        tmp="@SP\n"
        tmp+="D=M\n"
        tmp="@"+name+"\n"
        tmp+="D;JEQ\n"

    def writeArithmetic(self,command):
        print "write"
        if command=="add":
            tmp="@SP\n"
            tmp+="AM=M-1\n"
            tmp+="D=M\n"
            tmp+="@SP\n"
            tmp+="A=M-1\n"
            tmp+="M=D+M\n"
            self.output.write(tmp)
        elif command=="sub":
            tmp="@SP\n"
            tmp+="AM=M-1\n"
            tmp+="D=M\n"
            tmp+="@SP\n"
            tmp+="A=M-1\n"
            tmp+="M=M-D\n"
            self.output.write(tmp)
        elif command=="neg":
            tmp="@SP\n"
            tmp+="A=M-1\n"
            tmp+="M=-M\n"
            self.output.write(tmp)
        elif command=="and":
            tmp="@SP\n"
            tmp+="AM=M-1\n"
            tmp+="D=M\n"
            tmp+="@SP\n"
            tmp+="A=M-1\n"
            tmp+="M=D&M\n"
            self.output.write(tmp)
        elif command=="or":
            tmp="@SP\n"
            tmp+="AM=M-1\n"
            tmp+="D=M\n"
            tmp+="@SP\n"
            tmp+="A=M-1\n"
            tmp+="M=M|D\n"
            self.output.write(tmp)
        elif command=="not":
            tmp="@SP\n"
            tmp+="A=M-1\n"
            tmp+="M=!M\n"
            self.output.write(tmp)
        #boolean operator
        elif command=="eq":
            tmp="@SP\n"
            tmp+="AM=M-1\n"
            tmp+="D=M\n"
            tmp+="@SP\n"
            tmp+="A=M-1\n"
            tmp+="D=M-D\n"
            tmp+="@OP1." + str(self.bool_op) +"\n"
            tmp+="D;JEQ\n"
            tmp+="@SP\n"
            tmp+="A=M-1\n"
            tmp+="M=0\n"
            tmp+="@OP2." + str(self.bool_op) +"\n"
            tmp+="0;JMP\n"
            tmp+="(OP1."+str(self.bool_op)+")\n"
            tmp+="@SP\n"
            tmp+="A=M-1\n"
            tmp+="M=-1\n"
            tmp+="(OP2."+str(self.bool_op)+")\n"
            self.bool_op+=1
            self.output.write(tmp)
        elif command=="gt":
            tmp="@SP\n"
            tmp+="AM=M-1\n"
            tmp+="D=M\n"
            tmp+="@SP\n"
            tmp+="A=M-1\n"
            tmp+="D=M-D\n"
            tmp+="@OP1." + str(self.bool_op) +"\n"
            tmp+="D;JGT\n"
            tmp+="@SP\n"
            tmp+="A=M-1\n"
            tmp+="M=0\n"
            tmp+="@OP2." + str(self.bool_op) +"\n"
            tmp+="0;JMP\n"
            tmp+="(OP1."+str(self.bool_op)+")\n"
            tmp+="@SP\n"
            tmp+="A=M-1\n"
            tmp+="M=-1\n"
            tmp+="(OP2."+str(self.bool_op)+")\n"
            self.bool_op+=1
            self.output.write(tmp)
        elif command=="lt":
            tmp="@SP\n"
            tmp+="AM=M-1\n"
            tmp+="D=M\n"
            tmp+="@SP\n"
            tmp+="A=M-1\n"
            tmp+="D=M-D\n"
            tmp+="@OP1." + str(self.bool_op) +"\n"
            tmp+="D;JLT\n"
            tmp+="@SP\n"
            tmp+="A=M-1\n"
            tmp+="M=0\n"
            tmp+="@OP2." + str(self.bool_op) +"\n"
            tmp+="0;JMP\n"
            tmp+="(OP1."+str(self.bool_op)+")\n"
            tmp+="@SP\n"
            tmp+="A=M-1\n"
            tmp+="M=-1\n"
            tmp+="(OP2."+str(self.bool_op)+")\n"
            self.bool_op+=1
            self.output.write(tmp)

    def writePushPop(self,command,segment,index):
        if command=="C_PUSH":
            if segment=="constant":
                tmp="@"+index+"\n"
                tmp+="D=A\n"
                tmp+="@SP\n"
                tmp+="A=M\n"
                tmp+="M=D\n"
                tmp+="@SP\n"
                tmp+="M=M+1\n"
                self.output.write(tmp)
            elif segment in ["local","argument","this","that"]:
                tmp="@"+index+"\n"
                tmp+="D=A\n"
                tmp+="@"+segment_mapping[segment]+"\n"
                tmp+="A=D+M\n"
                tmp+="D=M\n"
                tmp+="@SP\n"
                tmp+="A=M\n"
                tmp+="M=D\n"
                tmp+="@SP\n"
                tmp+="M=M+1\n"
                self.output.write(tmp)
            elif segment=="pointer":
                tmp="@"+index+"\n"
                tmp+="D=A\n"
                tmp+="@3\n"
                tmp+="A=D+M\n"
                tmp+="D=M\n"
                tmp+="@SP\n"
                tmp+="A=M\n"
                tmp+="M=D\n"
                tmp+="@SP\n"
                tmp+="M=M+1\n"
                self.output.write(tmp)
            elif segment=="temp":
                tmp="@"+index+"\n"
                tmp+="D=A\n"
                tmp+="@5\n"
                tmp+="A=D+M\n"
                tmp+="D=M\n"
                tmp+="@SP\n"
                tmp+="A=M\n"
                tmp+="M=D\n"
                tmp+="@SP\n"
                tmp+="M=M+1\n"
                self.output.write(tmp)
            elif segment=="static":
                tmp="@"+os.path.basename(self.fileName)+"."+index+"\n"
                tmp+="D=M\n"
                tmp+="@SP\n"
                tmp+="A=M\n"
                tmp+="M=D\n"
                tmp+="@SP\n"
                tmp+="M=M+1\n"
                self.output.write(tmp)
        else:
            print "Writing pop instruction"
            if segment in ["local","argument","this","that"]:
                tmp="@"+index+"\n"
                tmp+="D=A\n"
                tmp+="@"+segment_mapping[segment]+"\n"
                tmp+="D=D+M\n"
                tmp+="@13\n" #temp value for storage location
                tmp+="M=D\n"
                tmp+="@SP\n"
                tmp+="AM=M-1\n"
                tmp+="D=M\n"
                tmp+="@13\n"
                tmp+="A=M\n"
                tmp+="M=D\n"
                self.output.write(tmp)
            elif segment=="pointer":
                tmp="@"+index+"\n"
                tmp+="D=A\n"
                tmp+="@3\n"
                tmp+="D=D+M\n"
                tmp+="@13\n" #temp value for storage location
                tmp+="M=D\n"
                tmp+="@SP\n"
                tmp+="AM=M-1\n"
                tmp+="D=M\n"
                tmp+="@13\n"
                tmp+="A=M\n"
                tmp+="M=D\n"
                self.output.write(tmp)
            elif segment=="temp":
                tmp="@"+index+"\n"
                tmp+="D=A\n"
                tmp+="@5\n"
                tmp+="D=D+M\n"
                tmp+="@13\n" #temp value for storage location
                tmp+="M=D\n"
                tmp+="@SP\n"
                tmp+="AM=M-1\n"
                tmp+="D=M\n"
                tmp+="@13\n"
                tmp+="A=M\n"
                tmp+="M=D\n"
                self.output.write(tmp)
            elif segment=="static":
                tmp="@"+os.path.basename(self.fileName)+"."+index+"\n"
                tmp+="D=A\n"
                tmp+="@13\n" #temp value for storage location
                tmp+="M=D\n"
                tmp+="@SP\n"
                tmp+="AM=M-1\n"
                tmp+="D=M\n"
                tmp+="@13\n"
                tmp+="A=M\n"
                tmp+="M=D\n"
                self.output.write(tmp)
                #self.static_count+=1
                pass
        pass

    def setFileName(self,name):
        self.fileName = name

    def close(self):
        self.output.close()

def process_file(asm_file,cw):
    p = Parser(asm_file)
    cw.setFileName(asm_file[:-3])
    while(p.hasMoreCommands()):
        print "parserloop"
        p.advance()
        if (p.commandType()=="C_ARITHMETIC"):
            print "arith"
            cw.writeArithmetic(p.arg1())
        elif (p.commandType()=="C_PUSH"):
            print "push"
            cw.writePushPop("C_PUSH",p.arg1(),p.arg2())
        elif (p.commandType()=="C_POP"):
            print "pop"
            cw.writePushPop("C_POP",p.arg1(),p.arg2())
        elif (p.commandType()=="C_LABEL"):
            cw.writeLabel(p.arg1())
        elif (p.commandType()=="C_FUNCTION"):
            pass
        elif (p.commandType()=="C_CALL"):
            pass
        elif (p.commandType()=="C_RETURN"):
            pass
        elif (p.commandType()=="C_GOTO"):
            cw.writeGoTo(p.arg1())
        elif (p.commandType()=="C_IF"):
            cw.writeIf(p.arg1())


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-d",dest="directory")
    group.add_argument("-f",dest="file")
    args=parser.parse_args()
    cw = CodeWriter("output.asm")
    print "Entered prog"
    #code to select between two modes
    if args.file is None:
        for (dirpath, dirnames, filenames) in os.walk(args.directory):
            for filename in filenames:
                if filename[-3:] == '.vm':
                    asm_file = os.sep.join([dirpath, filename])
                    process_file(asm_file,cw)
    else:
        print "in file"
        process_file(args.file,cw)


    cw.close()

if __name__ == '__main__':
    main()



