@17
D=A
@SP
A=M
M=D
@SP
M=M+1
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
@SP
A=M-1
D=M-D
@OP1.0
D;JEQ
@SP
A=M-1
M=0
@OP2.0
0;JMP
(OP1.0)
@SP
A=M-1
M=-1
(OP2.0)
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
@16
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
@SP
A=M-1
D=M-D
@OP1.1
D;JEQ
@SP
A=M-1
M=0
@OP2.1
0;JMP
(OP1.1)
@SP
A=M-1
M=-1
(OP2.1)
@16
D=A
@SP
A=M
M=D
@SP
M=M+1
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
@SP
A=M-1
D=M-D
@OP1.2
D;JEQ
@SP
A=M-1
M=0
@OP2.2
0;JMP
(OP1.2)
@SP
A=M-1
M=-1
(OP2.2)
@892
D=A
@SP
A=M
M=D
@SP
M=M+1
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
@SP
A=M-1
D=M-D
@OP1.3
D;JLT
@SP
A=M-1
M=0
@OP2.3
0;JMP
(OP1.3)
@SP
A=M-1
M=-1
(OP2.3)
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
@892
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
@SP
A=M-1
D=M-D
@OP1.4
D;JLT
@SP
A=M-1
M=0
@OP2.4
0;JMP
(OP1.4)
@SP
A=M-1
M=-1
(OP2.4)
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
@SP
A=M-1
D=M-D
@OP1.5
D;JLT
@SP
A=M-1
M=0
@OP2.5
0;JMP
(OP1.5)
@SP
A=M-1
M=-1
(OP2.5)
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
@SP
A=M-1
D=M-D
@OP1.6
D;JGT
@SP
A=M-1
M=0
@OP2.6
0;JMP
(OP1.6)
@SP
A=M-1
M=-1
(OP2.6)
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
@SP
A=M-1
D=M-D
@OP1.7
D;JGT
@SP
A=M-1
M=0
@OP2.7
0;JMP
(OP1.7)
@SP
A=M-1
M=-1
(OP2.7)
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
@SP
A=M-1
D=M-D
@OP1.8
D;JGT
@SP
A=M-1
M=0
@OP2.8
0;JMP
(OP1.8)
@SP
A=M-1
M=-1
(OP2.8)
@57
D=A
@SP
A=M
M=D
@SP
M=M+1
@31
D=A
@SP
A=M
M=D
@SP
M=M+1
@53
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
@SP
A=M-1
M=D+M
@112
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
@SP
A=M-1
M=M-D
@SP
A=M-1
M=-M
@SP
AM=M-1
D=M
@SP
A=M-1
M=D&M
@82
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
@SP
A=M-1
M=M|D
@SP
A=M-1
M=!M