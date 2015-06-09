
/*  Intro to payloads
	The goal of this assignment is to gain familiarity with the 
	environment in which stage 0 payloads run by writing a basic 
	payload that will be executed within the stack or heap of some 
	process. 
	
	Your assignment is to craft a 32-bit linux x86 assembly 
	language payload that opens a file named 'flag' in the current 
	directory and displays the contents of that file to stdout. 
	Once complete, your payload should exit cleanly with return 
	code 0. Your payload will be tested by assembling it with nasm 
	using “-f bin”, a program will then load your payload into its 
	memory space and transfer control to it. No parameters may be 
	passed into your payload. Successful execution will be judged 
	by comparing the output of the program with the actual contents 
	of the file named 'flag' 
	
	You must also create a second program, written in C whose purpose 
	is to load the binary machine code blob of the first program into 
	memory and then transfer control to the newly loaded bytes. This 
	program will receive a single command line argument that 
	represents the name of the assembled binary blob file. The best 
	way for you to proceed is probably to write a stand alone 
	assembly language program that performs the required task (
	reading and displaying 'flag') that makes no use of any fixed 
	addresses (no .data or .bss). Once you have a working program, 
	create a second program using C to read your payload from disk 
	and execute it. There are any number of ways to transfer control 
	to arbitrary locations in memory from a C program. If you are not 
	familiar with them, you may want to look into function pointers. 
	The following represents basic build and use of the two programs:
	
	# nasm -f bin assn1.asm
	# gcc -o assn1_harness assn1_harness.c
	# echo howdoyoulikemenow > flag
	# ./assn1_harness assn1
	howdoyoulikemenow
	#
	Notes:
	1. Depending on your Linux setup and how you write your test 
	   harness, you may need to make use of the execstack program 
	   to make the stack executable. 
	2. You may also wish to play around with the kernel variable: 
	   kernel.randomize_va_space which is available on some linux 
	   systems and which, when set to zero, disables address space 
	   layout randomization.
Basic code framework provided by:  Worked with Forest Bush.	
http://stackoverflow.com/questions/14002954  
*/
#include <stdio.h>
#include <stdlib.h>
 
int main ( int argc, char *argv[] )
{
	FILE *f = fopen(argv[1], "rb");
	fseek(f, 0, SEEK_END);
	long fsize = ftell(f);
	fseek(f, 0, SEEK_SET);

	char *string = malloc(fsize + 1);
	fread(string, fsize, 1, f);
	fclose(f);
    std::cout << "press any key to exit...";
	return 0;
}
