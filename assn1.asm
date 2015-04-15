BITS 32
; This Assembly Code will open a file named 'flag' 
;   in the current directory and displays contents
;	to stdout then it must exit cleanly and return code 0
;   The best way for you to proceed is probably to write a 
;   stand alone assembly language program that performs the 
;   required task (reading and displaying 'flag') that makes 
;   no use of any fixed addresses (no .data or .bss). Once you 
;   have a working program, create a second program using C to 
;   read your payload from disk and execute it. 
;   nasm -f bin assn1.asm