#!/usr/bin/env python3
from ctypes import addressof
import socket
import sys
import select

from tcp_client import *

class channel:
    def __init__(self, name: str, client: client) -> None:
        self.name = name
        self.clients = [client]
        self.admins = [client]
        self.owner = client
        self.capacity = 10

## Getters ##
    # returns the channel's name
    def get_name(self) -> str:
        return self.name
    # returns a list of all clients in the channel
    def get_clients(self) -> list[client]:
        return self.clients
    # returns a list of all admins of the channel
    def get_admins(self) -> list[client]:
        return self.admins
    # returns the owner of the channel
    def get_owner(self) -> client:
        return self.owner
    # returns the channel's capacity
    def get_capacity(self) -> int:
        return self.capacity

    # returns a list of all client's name in the channel
    def get_clients_name(self) -> list[str]:
        names = []
        for client in self.clients:
            names.append(client.get_name())

        return names
    # returns a list of all client's socket in the channel
    def get_clients_socket(self) -> list[object]:
        sockets = []
        for client in self.clients:
            sockets.append(client.get_socket())
        return sockets
    # returns a list of all admin's name in the channel
    def get_admins_name(self) -> list[str]:
        names = []
        for admin in self.admins:
            names.append(admin.get_name())
        return names
    # returns a list of all admin's socket in the channel
    def get_admins_socket(self) -> list[object]:
        sockets = []
        for admin in self.admins:
            sockets.append(admin.get_socket())
        return sockets

## Setters ##
    # sets the channel's name
    def set_name(self, name: str) -> None:
        self.name = name

## Modifiers ##
    # adds a client to the channel
    def add_client(self, client: client) -> bool:
        if client not in self.clients:
            self.clients.append(client)
            return True
        return False
    # removes a client from the channel
    def remove_client(self, client: client) -> bool:
        if client in self.clients:
            if client == self.owner:
                return False
            self.clients.remove(client)
            if client in self.admins:
                self.admins.remove(client)
            return True
        return False
    # Add a client to the admin list
    def promote(self, client: client) -> bool:
        if client in self.clients:
            self.admins.append(client)
            self.msg_to(client, "You have been promoted to admin on channel [" + self.name + "] by " + self.owner.name)
            return True
        return False
    # Removes a client from the admin list
    def demote(self, client: client) -> bool:
        if client in self.admins:
            self.admins.remove(client)
            return True
        return False



    # Search for a client by name
    def client_by_name(self, name) -> client:
        for client in self.clients:
            if client.get_name() == name:
                return client
        return None
    # Search for a client by socket
    def client_by_socket(self, sock) -> client:
        for client in self.clients:
            if client.get_socket() == sock:
                return client
        return None

##  Utils  ##
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
    def msg_clients(self, message) -> None:
        if message[-1] != '\n':
            message += '\n'
        for client in self.clients:
            client.msg(message)
    # send a message to all admins in the channel
    def msg_admins(self, message) -> None:
        if message[-1] != '\n':
            message += '\n'
        for admin in self.admins:
            admin.msg(message)
    # send a message to the owner of the channel
    def msg_owner(self, message) -> None:
        if message[-1] != '\n':
            message += '\n'
        self.owner.msg(message)
    # show log information
    def log(self, message) -> None:
        print(message)
