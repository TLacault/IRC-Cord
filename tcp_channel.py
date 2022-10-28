#!/usr/bin/env python3
from ctypes import addressof
import socket
import sys
import select

from tcp_client import *

class channel:
    def __init__(self, name, client):
        self.name = name
        self.admins = []
        self.clients = [client]
        self.promote(client)

##  Client Management  ##
    def add_client(self, client):
        if client not in self.clients:
            self.clients.append(client)
            return True
        return False
    def remove_client(self, client):
        if client in self.clients:
            self.clients.remove(client)
            if client in self.admins:
                self.admins.remove(client)
            return True
        return False

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

##  Admin Management  ##
    def promote(self, admin):
        if admin in self.clients:
            self.admins.append(admin)
            return True
        return False
    def demote(self, admin):
        if admin in self.admins:
            self.admins.remove(admin)
            return True
        return False

    def admin_names(self):
        names = []
        for admin in self.admins:
            names.append(admin.name)
        return names
    def admin_by_name(self, name):
        for admin in self.admins:
            if admin.name == name:
                return admin
        return None
    def admin_sockets(self):
        sockets = []
        for admin in self.admins:
            sockets.append(admin.sock)
        return sockets
    def admin_by_socket(self, sock):
        for admin in self.admins:
            if admin.sock == sock:
                return admin
        return None

##  Communication  ##
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
