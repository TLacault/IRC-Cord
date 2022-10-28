#!/usr/bin/env python3
from ctypes import addressof
import socket
import sys
import select

from tcp_client import *
from tcp_channel import *

class server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.clients = []
        self.channels = []

        self.sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM, 0)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.sock.listen(1)

        self.add_client(self.sock, "server")
        self.add_channel("main", self.clients[0])
        self.add_channel("other", self.clients[0])

    def add_client(self, sock, name):
        self.clients.append(client(sock, name))
    def client_sockets(self):
        sockets = []
        for client in self.clients:
            sockets.append(client.sock)
        return sockets
    def client_by_socket(self, sock):
        for client in self.clients:
            if client.sock == sock:
                return client
        return None
    def client_names(self):
        names = []
        for client in self.clients:
            names.append(client.name)
        return names
    def client_by_name(self, name):
        for client in self.clients:
            if client.name == name:
                return client
        return None

    def add_channel(self, name, admin):
        self.channels.append(channel(name, admin))
    def channel_names(self):
        names = []
        for channel in self.channels:
            names.append(channel.name)
        return names
    def channel_by_name(self, name):
        for channel in self.channels:
            if channel.name == name:
                return channel
        return None

    def show(self):
        print("<<<<  SERVER  >>>>")
        print("Host: " + self.host)
        print("Port: " + str(self.port))
        for client in self.clients:
            client.show()
        for channel in self.channels:
            channel.show()
        print(">>>>  SERVER  <<<<")
