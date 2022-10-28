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

##  Client Management  ##
    # adds a client to the server
    def add_client(self, sock, addr):
        self.clients.append(client(sock, addr))
    # removes a client from the server
    def remove_client(self, client):
        self.clients.remove(client)
    # returns a list of all client's sockets on the server
    def client_sockets(self):
        sockets = []
        for client in self.clients:
            sockets.append(client.sock)
        return sockets
    # search for a client by socket and return the client
    def client_by_socket(self, sock):
        for client in self.clients:
            if client.sock == sock:
                return client
        return None
    # returns a list of all clients names on the server
    def client_names(self):
        names = []
        for client in self.clients:
            names.append(client.name)
        return names
    # search for a client by name and return the client
    def client_by_name(self, name):
        for client in self.clients:
            if client.name == name:
                return client
        return None
    # returns a list of all client's addresses on the server
    def client_addresses(self):
        addresses = []
        for client in self.clients:
                addresses.append(client.addr)
        return addresses
    # search for a client by address and return the client
    def client_by_address(self, addr):
        for client in self.clients:
            if client.addr == addr:
                return client
        return None
    # return a list of all client's ports on the server
    def client_ports(self):
        ports = []
        for client in self.clients:
            ports.append(int(client.port))
        return ports
    # search for a client by port and return the client
    def client_by_port(self, port):
        for client in self.clients:
            if client.port == port:
                return client
        return None

##  Channel Management  ##
    # creates a channel on the server
    def add_channel(self, name, admin):
        self.channels.append(channel(name, admin))
    # deletes a channel from the server
    def remove_channel(self, channel):
        self.channels.remove(channel)
    # returns a list of all channels names present on the server
    def channel_names(self):
        names = []
        for channel in self.channels:
            names.append(channel.name)
        return names
    # returns a list of all clients present on a channel
    def channel_clients(self, channel_name):
        clients = []
        channel = self.channel_by_name(channel_name)
        for client in channel.clients:
            clients.append(client)
        return clients
    # returns a list of all admins present on a channel
    def channel_admins(self, channel_name):
        admins = []
        channel = self.channel_by_name(channel_name)
        for admin in channel.admins:
            admins.append(admin)
        return admins
    # search for a channel by name and return the channel
    def channel_by_name(self, name):
        for channel in self.channels:
            if channel.name == name:
                return channel
        return None
    # search for a channel by client and return the channel
    def channel_by_client(self, client):
        channels = []
        for channel in self.channels:
            if client in channel.clients:
                channels.append(channel)
        return channels
    # search for a channel by admin and return the channel
    def channel_by_admin(self, admin):
        channels = []
        for channel in self.channels:
            if admin in channel.admins:
                channels.append(channel)
        return channels

##  Server Management  ##
    # show all server's properties
    def show(self):
        print("<<<<  SERVER  >>>>")
        print("Host: " + self.host)
        print("Port: " + str(self.port))
        for client in self.clients:
            client.show()
        for channel in self.channels:
            channel.show()
        print(">>>>  SERVER  <<<<")
