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
;   Stack setup
;   		filename (8 bytes 'flag',0x0)
;   ebp->   charbuf (4 byte)
section .text
global main    ;allows gcc to find function

_main:
push ebp      ;save caller frame ptr
mov ebp, esp  ;setup our frame ptr
sub esp, 16   ;allocate local storage

call open
.looptop:
call read
call write
check for eof
if not eof jump .looptop
call close

mov esp, ebp  ;deallocate locals
pop ebp   	  ;restore callers frame ptr
ret 0
;open file called flag   eax=5(open) ebx=filenameptr ecx=flags   edx=mode
.read:
mov ecx, 0   ;mode=RDonly=0  WRonly=1  RDRW=2  
mov ebx, 'flag'  ;name of file to open
mov eax, 5    ;open syscall
int 0x80
;read flag               eax=3(read)   ebx=filedescripter  ecx=(bufptr)   edx=(size)
;display flag    eax=4(write)  ebx=1(stdout fd)  ecx=(bufptr)  edx=(size)
;close flag   eax=6(close)   ebx=(fd)