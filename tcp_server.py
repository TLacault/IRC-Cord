#!/usr/bin/env python3
from ctypes import addressof
import socket
import sys
import select

from tcp_client import *
from tcp_channel import *

class server:
    def __init__(self, host = "", port = 7777, name = "default server"):
        self.host = host
        self.port = port
        self.name = name
        self.clients = []
        self.channels = []

        self.socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM, 0)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))
        self.socket.listen(1)

##  Client Management  ##
    # adds a client to the server taking a socket and address as parameter
    def add_client(self, sock, addr) -> bool:
        new_client = client(sock, addr)
        if new_client not in self.clients:
            self.clients.append(new_client)
            return True
        return False
    # adds a client to the server taking a client as parameter
    def add_client_copy(self, client) -> bool:
        if client not in self.clients:
            self.clients.append(client)
            return True
        return False
    # removes a client from the server
    def remove_client(self, client) -> bool:
        for channel in self.channel_by_client(client):
            channel.remove_client(client)
        if client in self.clients:
            self.clients.remove(client)
            client.close()
            return True
        return False

    # returns a list with server's socket + all client's socket on the server
    def all_sockets(self) -> list:
        return [self.socket] + self.client_sockets()
    # returns a list of all client's socket on the server
    def client_sockets(self) -> list:
        sockets = []
        for client in self.clients:
            sockets.append(client.socket)
        return sockets
    # returns a list with server's name + all client's name on the server
    def all_names(self) -> list:
        return [self.name] + self.client_names()
    # returns a list of all client's name on the server
    def client_names(self) -> list:
        names = []
        for client in self.clients:
            names.append(client.name)
        return names
    # returns a list of all client's address on the server
    def client_addresses(self) -> list:
        addresses = []
        for client in self.clients:
                addresses.append(client.address)
        return addresses
    # return a list of all client's port on the server
    def client_ports(self) -> list:
        ports = []
        for client in self.clients:
            ports.append(int(client.port))
        return ports

    # search for a client by socket and return the client
    def client_by_socket(self, sock) -> client:
        for client in self.clients:
            if client.socket == sock:
                return client
        return None
    # search for a client by name and return the client
    def client_by_name(self, name) -> client:
        for client in self.clients:
            if client.name == name:
                return client
        return None
    # search for a client by address and return the client
    def client_by_address(self, addr) -> client:
        for client in self.clients:
            if client.address == addr:
                return client
        return None
    # search for a client by port and return the client
    def client_by_port(self, port) -> client:
        for client in self.clients:
            if client.port == port:
                return client
        return None

##  Channel Management  ##
    # creates a channel on the server
    def add_channel(self, name, admin) -> bool:
        if name not in self.channel_names():
            self.channels.append(channel(name, admin))
            return True
        return False
    # deletes a channel from the server
    def remove_channel(self, channel) -> bool:
        if channel in self.channels:
            self.channels.remove(channel)
            return True
        return False

    # returns a list of all channel's name present on the server
    def channel_names(self) -> list:
        names = []
        for channel in self.channels:
            names.append(channel.name)
        return names
    # returns a list of all clients present on a channel
    def channel_clients(self, channel_name) -> list:
        clients = []
        channel = self.channel_by_name(channel_name)
        for client in channel.clients:
            clients.append(client)
        return clients
    # returns a list of all admins present on a channel
    def channel_admins(self, channel_name) -> list:
        admins = []
        channel = self.channel_by_name(channel_name)
        for admin in channel.admins:
            admins.append(admin)
        return admins

    # search for a channel by name and return the channel
    def channel_by_name(self, name) -> channel:
        for channel in self.channels:
            if channel.name == name:
                return channel
        return None
    # search for a channel by client and return the channel
    def channel_by_client(self, client) -> list:
        channels = []
        for channel in self.channels:
            if client in channel.clients:
                channels.append(channel)
        return channels
    # search for a channel by admin and return the channel
    def channel_by_admin(self, admin) -> list:
        channels = []
        for channel in self.channels:
            if admin in channel.admins:
                channels.append(channel)
        return channels

## Commands ##
    # server sends a message to every client on the server
    def broadcast(self, message) -> None:
        msg = "[server] " + message
        for client in self.clients:
            self.msg_to(client, msg)

    # modifies the name of the client if it is not taken
    def nick(self, client_names: list[str], data: str) -> None:
        nick = data.replace(" ", "")
        nick = nick.replace("\t", "")
        nick = nick.replace("\n", "")
        if nick not in client_names:
            if nick.strip() != "":
                if nick[-1] == '\n':
                    nick = nick[:-1]
                self.log("client [" + client.name + "] => [" + nick + "]")
                self.msg("[server] name changed to [" + nick + "]")
                self.name = nick
            else:
                self.usage_nick(client)
        else:
            self.msg("[server] nickname is already taken")

    # removes a client from the server and every channel
    def quit(self, server) -> None:
        server.remove_client(self)
        server.broadcast(self.name + " has left the server")
        server.log("client [" + client.name + "] disconnected")
    # shows client's details
    def info(self, channel_names: list[str]) -> None:
        self.msg("[client:name] " + client.name)
        msg_channels = "[client:channels] "
        for channel in channel_names:
            msg_channels += channel + ", "
        if msg_channels[-2:] == ", ":
            msg_channels = msg_channels[:-2]
        else:
            msg_channels += "try /channel_help"
        self.msg(msg_channels)
    # shows the client's network information
    def info_net(self) -> None:
        self.msg("[client:socket] " + str(self.socket))
        self.msg("[client:address] " + self.address)
        self.msg("[client:port] " + self.port)

    # sends a list of all client's name on the server
    def names(self: object, client_names: list[str]) -> None:
        client_names = ", ".join(client_names)
        self.msg("[server] " + client_names)

    # def usage_msg(self, client) -> None:
    #     self.msg_to(client, "[server] usage: /msg <channel> <message>")
    # def msg(self, client, data) -> None:
    #     channel_name = data.split(" ")[0]
    #     if channel_name in self.channel_names():
    #         channel = self.channel_by_name(channel_name)
    #         if client not in channel.clients:
    #             try:
    #                 message = data.split(" ", 1)[1]
    #             except IndexError:
    #                 self.usage_msg(client)
    #                 return
    #             channel.msg(client, message)
    #         else:
    #             # join channel
    #             channel.add_client(client)
    #     else:
    #         #create channel


    def cmd(self, data, client) -> None:
        if data[0] == '/':
            cmd = data[1:].split(' ')[0]
            cmd = cmd.replace("\n", "")
            if cmd == 'nick':
                client.nick(data[6:])
            elif cmd == "msg":
                self.msg(client, data[5:])
            elif cmd == 'names':
                self.names(client)
            elif cmd == 'info':
                self.info(client)
            elif cmd == 'info-net':
                self.info_net(client)
            elif cmd == 'quit':
                self.quit(client)
            else:
                self.msg_to(client, "[server] invalid command\n")
        else:
            self.msg_to(client, "[server] invalid command\n")

##  Server Management  ##
    # show log information
    def log(self, message) -> None:
        print(message)

    # show all server's properties
    def show(self) -> None:
        print("<<<<  SERVER  >>>>")
        print("Name: " + self.name)
        if self.host == "":
            print("Host: " + "localhost")
        else:
            print("Host: " + self.host)
        print("Port: " + str(self.port))
        for client in self.clients:
            client.show()
        for channel in self.channels:
            channel.show()
        print(">>>>  SERVER  <<<<\n")
