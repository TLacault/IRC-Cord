#!/usr/bin/env python3
from ctypes import addressof
import socket
import sys
import select

class client:
    def __init__(self, sock, addr):
        self.socket = sock
        self.address = str(addr[0])
        self.port = str(addr[1])
        self.name = self.address + ':' + self.port

##  Client Management  ##
    # shows all client's information
    def show(self) -> None:
        print("< CLIENT >")
        print("Socket: " + str(self.socket))
        print("Address: " + self.address)
        print("Port: " + self.port)
        print("Name: " + self.name)
