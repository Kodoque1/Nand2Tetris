import Config

class VMWriter:
    def __init__(self,output):
        self.output=output

    def writePush(self,segment,index):
        self.output.write("push " + str(Config.dict_segment[segment]) + " " + str(index) +"\n")

    def writePop(self,segment,index):
        self.output.write("pop " + str(Config.dict_segment[segment]) + " " + str(index) +"\n")

    def WriteArithmetic(self,command):
        #print command
        self.output.write(str(Config.dict_arithmetic[command])+"\n")

    def WriteLabel(self,label):
        self.output.write("label " + str(label) + "\n")

    def WriteGoto(self,label):
        self.output.write("goto " + str(label) + "\n")

    def WriteIf(self,label):
        self.output.write("goto " + str(label) + "\n")

    def WriteCall(self,name,nArgs):
        self.output.write("call " + str(name) + " " + str(nArgs) + "\n")

    def WriteFunction(self,name,nLocals):
        self.output.write("function " + str(name) + " " + str(nLocals) + "\n")

    def writeReturn(self):
        self.output.write("return\n")

    def close(self):
        self.output.close()
