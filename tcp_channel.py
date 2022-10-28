#!/usr/bin/env python3
from ctypes import addressof
import socket
import sys
import select

from tcp_client import *

class channel:
    def __init__(self, name, admin):
        self.name = name
        self.clients = [admin]
        self.admins = [admin]

    def c_names(self):
        names = []
        for client in self.clients:
            names.append(client.name)
        return names
    def c_by_name(self, name):
        for client in self.clients:
            if client.name == name:
                return client
        return None
    def c_sockets(self):
        sockets = []
        for client in self.clients:
            sockets.append(client.sock)
        return sockets
    def c_by_socket(self, sock):
        for client in self.clients:
            if client.sock == sock:
                return client
        return None

    def join(self, client):
        self.clients.append(client)
    def leave(self, client):
        self.clients.remove(client)
    def msg(self, msg):
        for client in self.clients:
            client.sendall(msg.encode("utf-8"))

    def show(self):
        print("\n<< CHANNEL >>")
        print("Name: " + self.name)
        print(">> ADMINS:")
        for user in self.admins:
            user.show()
        print(">> CLIENTS:")
        for user in self.clients:
            if user not in self.admins:
                user.show()
