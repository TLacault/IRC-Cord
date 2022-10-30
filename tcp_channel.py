#!/usr/bin/env python3
import socket as Socket
from tcp_client import *

class Channel:
    def __init__(self, name: str, client: Client) -> None:
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
    def get_clients(self) -> list[Client]:
        return self.clients
    # returns a list of all admins of the channel
    def get_admins(self) -> list[Client]:
        return self.admins
    # returns the owner of the channel
    def get_owner(self) -> Client:
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
    # sets the channel's client list
    def set_clients(self, clients: list[Client]) -> None:
        self.clients = clients
    # sets the channel's admins list
    def set_admins(self, admins: list[Client]) -> None:
        self.admins = admins
    # sets the channel's owner
    def set_owner(self, client: Client) -> None:
        self.owner = client
    # sets the channel's capacity
    def set_capacity(self, capacity: int) -> None:
        self.capacity = capacity

## Modifiers ##
    # adds a client to the channel
    def add_client(self, client: Client) -> bool:
        if client not in self.clients:
            self.clients.append(client)
            return True
        return False
    # removes a client from the channel
    def remove_client(self, client: Client) -> bool:
        if client in self.clients:
            if client == self.owner:
                return False
            self.clients.remove(client)
            if client in self.admins:
                self.admins.remove(client)
            return True
        return False
    # Add a client to the admin list
    def add_admin(self, client: Client) -> bool:
        if client in self.clients:
            self.admins.append(client)
            return True
        return False
    # Removes a client from the admin list
    def remove_admin(self, client: Client) -> bool:
        if client in self.admins:
            self.admins.remove(client)
            return True
        return False

## Search ##
    # Search for a client by name
    def client_by_name(self, name: str) -> Client:
        for client in self.clients:
            if client.get_name() == name:
                return client
        return None
    # Search for a client by socket
    def client_by_socket(self, socket: Socket) -> Client:
        for client in self.clients:
            if client.get_socket() == socket:
                return client
        return None
    # search for an admin by name
    def admin_by_name(self, name: str) -> Client:
        for admin in self.admins:
            if admin.get_name() == name:
                return admin
        return None
    # search for an admin by socket
    def admin_by_socket(self, socket: Socket) -> Client:
        for admin in self.admins:
            if admin.get_socket() == socket:
                return admin
        return None

##  Communication  ##
    # send a message to all clients in the channel
    def msg_clients(self, message: str) -> None:
        if message[-1] != '\n':
            message += '\n'
        for client in self.clients:
            client.msg(message)
    # send a message to all admins in the channel
    def msg_admins(self, message: str) -> None:
        if message[-1] != '\n':
            message += '\n'
        for admin in self.admins:
            admin.msg(message)
    # send a message to the owner of the channel
    def msg_owner(self, message: str) -> None:
        if message[-1] != '\n':
            message += '\n'
        self.owner.msg(message)
    # show log information
    def log(self, message: str) -> None:
        print(message)
