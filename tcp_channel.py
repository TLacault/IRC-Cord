#!/usr/bin/env python3
from ctypes import addressof
import socket
import sys
import select

from tcp_client import *

class channel:
    def __init__(self, name, client):
        self.name = name
        self.clients = [client]
        self.admins = []
        self.promote(client)

##  Client Management  ##
    # add a client to the channel
    def add_client(self, client) -> bool:
        if client not in self.clients:
            self.clients.append(client)
            return True
        return False
    # removes a client from the channel
    def remove_client(self, client) -> bool:
        if client in self.clients:
            self.clients.remove(client)
            if client in self.admins:
                self.admins.remove(client)
            return True
        return False

    # returns a list of all client's name in the channel
    def client_names(self) -> list:
        names = []
        for client in self.clients:
            names.append(client.name)
        return names
    # returns a list of all client's socket in the channel
    def client_sockets(self) -> list:
        sockets = []
        for client in self.clients:
            sockets.append(client.socket)
        return sockets

    # Search for a client by name
    def client_by_name(self, name) -> client:
        for client in self.clients:
            if client.name == name:
                return client
        return None
    # Search for a client by socket
    def client_by_socket(self, sock) -> client:
        for client in self.clients:
            if client.socket == sock:
                return client
        return None

##  Admin Management  ##
    # Add a client to the admin list
    def promote(self, admin) -> bool:
        if admin in self.clients:
            self.admins.append(admin)
            return True
        return False
    # Removes a client from the admin list
    def demote(self, admin) -> bool:
        if admin in self.admins:
            self.admins.remove(admin)
            return True
        return False

    # returns a list of all admin's name in the channel
    def admin_names(self) -> list:
        names = []
        for admin in self.admins:
            names.append(admin.name)
        return names
    # returns a list of all admin's socket in the channel
    def admin_sockets(self) -> list:
        sockets = []
        for admin in self.admins:
            sockets.append(admin.socket)
        return sockets

    # search for an admin by name
    def admin_by_name(self, name) -> client:
        for admin in self.admins:
            if admin.name == name:
                return admin
        return None
    # search for an admin by socket
    def admin_by_socket(self, sock) -> client:
        for admin in self.admins:
            if admin.socket == sock:
                return admin
        return None

##  Communication  ##
    # send a message to all clients in the channel
    def msg(self, msg) -> None:
        for client in self.clients:
            client.sendall(msg.encode("utf-8"))

## Channel Management  ##
    # shows all channel's properties
    def show(self) -> None:
        print("\n<< CHANNEL >>")
        print("Name: " + self.name)
        print(">> ADMINS:")
        for user in self.admins:
            user.show()
        print(">> CLIENTS:")
        for user in self.clients:
            if user not in self.admins:
                user.show()
