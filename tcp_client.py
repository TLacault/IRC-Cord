#!/usr/bin/env python3
from ctypes import addressof
import socket
import sys
import select

class client:
    def __init__(self, sock, name):
        self.sock = sock
        self.name = name

    def show(self):
        print("< CLIENT >")
        print("Name: " + self.name)
        print("Socket: " + str(self.sock))
