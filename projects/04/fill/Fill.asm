// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, the
// program clears the screen, i.e. writes "white" in every pixel.

// Put your code here.

(INIT)

// Loading pointer with start of screen
@SCREEN
D=A
@i //Pointer to screen
M=D

(LOOP)


	//0 or 1 for Keypressed
	@KBD
	D=M
	@ZERO
	D;JEQ
	@1
	D=-A
	(ZERO)
	
	//Writing keyboard value to screen
	@i
	A=M
	M=D

	//inc i
	@i
	M=M+1

	//Reinit if needed

	@i // end of screen memory
	D=M
	@24575
	D=D-A
	@INIT
	D;JGT

@LOOP
0;JMP