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
section .text
global _start    ;allows gcc to find function
;
_start:
push ebp      ;save caller frame ptr
mov ebp, esp  ;setup our frame ptr
sub esp, 16   ;allocate local storage
;   Stack setup
;           filedescripter (4 bytes)
;   		filename (8 bytes 'flag',0x0)
;   ebp->   charbuf (4 byte)
;OPEN flag eax=5(open) ebx=filenameptr ecx=flags   edx=mode
;open file called flag   
; flag0 in little indian hex= 0x67 'g' 0x61 'a', 0x6c 'l', 0x66 'f', 
;     0x0 'null' 
mov eax, 0x616c6622
mov [ebp+4], eax
mov eax, 0x00002267
mov [ebp+8], eax
mov ecx, 0   ;mode=RDonly=0  WRonly=1  RDRW=2  
mov ebx, [ebp+4]  ;name of file to open
mov eax, 5    ;open syscall
int 0x80
mov [ebp+12], eax  ;capture filedescripter number of file
; Start loop that will alternate between reading characters 
;           and writing to standard out
;.looptop:
;READ flag   eax=3(read)   ebx=filedescripter  ecx=(bufptr)   edx=(size)
; read a single character from flag
;WRITE flag    eax=4(write)  ebx=1(stdout fd)  ecx=(bufptr)  edx=(size)
; write a single character to stdout
; check for eof
; if not eof jump .looptop
;CLOSE flag   eax=6(close)   ebx=(fd)
; close file
mov ebx, [ebp+12]   ;move fd for opened file into ebx
mov eax, 6   		;sys_close systemcall number
int 0x80
mov esp, ebp  ;deallocate locals
pop ebp   	  ;restore callers frame ptr
ret 0