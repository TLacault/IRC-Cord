#!/usr/bin/env python3
from ctypes import addressof
import socket
import sys
import select

class client:
    def __init__(self, sock, addr):
        self.sock = sock
        self.address = str(addr[0])
        self.port = str(addr[1])
        self.name = self.addr + ':' + self.port

    def show(self):
        print("< CLIENT >")
        print("Name: " + self.name)
        print("Socket: " + str(self.sock))
