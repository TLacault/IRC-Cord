#!/usr/bin/env python3
import socket as Socket
from tcp_client import *
from tcp_channel import *

class Server:
    def __init__(self, host = "", port = 7777, name = "server"):
        self.name = name
        self.host = host
        self.port = port
        self.clients = []
        self.channels = []

        self.socket = Socket.socket(Socket.AF_INET6, Socket.SOCK_STREAM, 0)
        self.socket.setsockopt(Socket.SOL_SOCKET, Socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))
        self.socket.listen(1)

## Getters ##
    # returns the server's name
    def get_name(self) -> str:
        return self.name
    # returns the server's host
    def get_host(self) -> str:
        return self.host
    # returns the server's host formatted in a string
    def get_host_formatted(self) -> str:
        if self.host == "":
            return "localhost"
        return self.host
    # returns the server's port
    def get_port(self) -> int:
        return self.port
    # returns the server's socket
    def get_socket(self) -> Socket:
        return self.socket
    # returns a list of all clients present on the server
    def get_clients(self) -> list[Client]:
        return self.clients
    # returns a list of all channels present on the server
    def get_channels(self) -> list[Channel]:
        return self.channels

    # returns a list with server's socket + all client's socket on the server
    def get_all_sockets(self) -> list:
        return [self.get_socket()] + self.get_clients_socket()
    # returns a list of all client's socket on the server
    def get_clients_socket(self) -> list:
        sockets = []
        for client in self.clients:
            sockets.append(client.get_socket())
        return sockets
    # returns a list with server's name + all client's name on the server
    def get_all_names(self) -> list[str]:
        return [self.name] + self.get_clients_name()
    # returns a list of all client's name on the server
    def get_clients_name(self) -> list[str]:
        names = []
        for client in self.clients:
            names.append(client.get_name())
        return names
    # returns a list of all client's name on the server formatted in a string
    def get_clients_name_formatted(self) -> str:
        names = ", ".join(self.get_clients_name())
        if names[-2:] == ", ":
            names = names[:-2]
        return names
    # returns a list of all client's address on the server
    def get_clients_address(self) -> list[str]:
        addresses = []
        for client in self.clients:
                addresses.append(client.get_address())
        return addresses
    # return a list of all client's port on the server
    def get_clients_port(self) -> list[int]:
        ports = []
        for client in self.clients:
            ports.append(client.get_port())
        return ports

    # returns a list of all channel's name present on the server
    def get_channels_name(self) -> list[str]:
        names = []
        for channel in self.channels:
            names.append(channel.get_name())
        return names
    # returns a list of all client's name on the server formatted in a string
    def get_channels_name_formatted(self) -> str:
        names = ", ".join(self.get_channels_name())
        if names[-2:] == ", ":
            names = names[:-2]
        return names

## Setters ##
    # sets the server's name
    def set_name(self, name: str) -> None:
        self.name = name
    # sets the server's host
    def set_host(self, host: str) -> None:
        self.host = host
    # sets the server's port
    def set_port(self, port: int) -> None:
        self.port = port
    # sets the server's socket
    def set_socket(self, socket: Socket) -> None:
        self.socket = socket
    # sets the server's client list
    def set_clients(self, clients: list[Client]) -> None:
        self.clients = clients
    # sets the server's channel list
    def set_channels(self, channels: list[Channel]) -> None:
        self.channels = channels

##  Modifiers  ##
    # creates a new client and add it to the server
    def add_client_create(self, socket: Socket, address: str) -> bool:
        new_client = client(socket, address)
        if new_client not in self.clients:
            self.clients.append(new_client)
            return True
        return False
    # adds a client to the server
    def add_client(self, client: Client) -> bool:
        if client not in self.clients:
            self.clients.append(client)
            return True
        return False
    # removes a client from the server and all channels he is in
    def remove_client(self, client: Client) -> bool:
        if client in self.clients:
            for channel in self.channels_by_client(client):
                channel.remove_client(client)
            self.clients.remove(client)
            return True
        return False

    # creates a channel on the server
    def add_channel_create(self, name: str, owner: Client) -> bool:
        new_channel = Channel(name, owner)
        if name not in self.get_channels_name():
            self.channels.append(new_channel)
            return True
        return False
    # adds a channel to the server
    def add_channel(self, channel: Channel) -> bool:
        if channel.get_name() not in self.get_channels_name():
            self.channels.append(channel)
            return True
        return False
    # deletes a channel from the server
    def remove_channel(self, channel: Channel) -> bool:
        if channel in self.channels:
            self.channels.remove(channel)
            return True
        return False

## Search ##
    # search for a client by socket and return the client
    def client_by_socket(self, socket: Socket) -> Client:
        for client in self.clients:
            if client.get_socket() == socket:
                return client
        return None
    # search for a client by name and return the client
    def client_by_name(self, name: str) -> Client:
        for client in self.clients:
            if client.get_name() == name:
                return client
        return None
    # returns a list of all client that has the address passed as parameter
    def clients_by_address(self, address: str) -> list[Client]:
        clients = []
        for client in self.clients:
            if client.get_address() == address:
                clients.append(client)
        return clients
    # returns a list of all client that has the port passed as parameter
    def clients_by_port(self, port: int) -> list[Client]:
        clients = []
        for client in self.clients:
            if client.get_port() == port:
                clients.append(client)
        return clients

    # search for a channel by name and return the channel
    def channel_by_name(self, name: str) -> Channel:
        for channel in self.channels:
            if channel.get_name() == name:
                return channel
        return None
    # returns a list of all channels the client is in
    def channels_by_client(self, client: Client) -> list[Channel]:
        channels = []
        for channel in self.channels:
            if client in channel.get_clients():
                channels.append(channel)
        return channels
    # returns a list of all channels name the client is in
    def channels_name_by_client(self, client: Client) -> list[str]:
        names = []
        for channel in self.channels_by_client(client):
            names.append(channel.get_name())
        return names
    # returns a list of all channels name the client is in a formatted in a string
    def channels_name_by_client_formatted(self, client: Client) -> str:
        channels = ", ".join(self.channels_name_by_client(client))
        if channels[-2:] == ", ":
            channels = channels[:-2]
        return channels
    # returns a list of all channels the admin is in
    def channels_by_admin(self, admin: Client) -> list:
        channels = [Channel]
        for channel in self.channels:
            if admin in channel.get_admins():
                channels.append(channel)
        return channels

## User Commands ##
    # modifies the name of the client if it is not taken
    def nick(self, client: Client, nick: str) -> None:
        nick = ''.join(nick.split())
        if nick not in self.get_all_names() + [self.name]:
            if nick.strip() != "":
                self.log("client [" + client.get_name() + "] => [" + nick + "]")
                client.msg("[server] name changed to [" + nick + "]")
                client.set_name(nick)
            else:
                self.usage_nick(client)
        else:
            client.msg("[server] nickname is already taken")
    # removes a client from the server and every channel
    def quit(self, client: Client, input: str) -> None:
        self.remove_client(client)
        self.broadcast(client.get_name() + " has left the server")
        self.log("client [" + client.get_name() + "] disconnected")
        client.close()
    # sends a list of all client's name on the server to the client
    def names(self, client: Client, input: str) -> None:
        client.msg("[server] " + self.get_clients_name_formatted())

## Channel Commands ##
    # sends a list of all channel's name on the server to the client
    def channel_list(self, client: Client, input: str) -> None:
        client.msg("[channels] " + self.get_channels_name_formatted())
    # promote to admin a client in a channel
    def promote(self, client: Client, input: str) -> None:
        try:
            channel_name = input.split()[0]
            name = ''.join(input.split()[1:])
        except IndexError:
            self.usage_promote(client)
            return
        if not channel_name or not name:
            self.usage_promote(client)
            return
        channel = self.channel_by_name(channel_name)
        if not channel:
            client.msg("[server] channel [" + channel_name + "] does not exist")
            return
        if client not in channel.get_admins():
            client.msg("[server] you are not an admin of [" + channel_name + "]")
            return
        admin = self.client_by_name(name)
        if not admin:
            client.msg("[server] client [" + name + "] does not exist")
            return
        if admin not in channel.get_clients():
            client.msg("[server] client [" + name + "] is not member of [" + channel_name + "]")
            return
        if admin in channel.get_admins():
            client.msg("[server] client [" + name + "] is already an admin")
            return
        channel.add_admin(admin)
        channel.broadcast("[" + channel.get_name() + "] client [" + name + "] promoted to admin by [" + client.get_name() + "]")
    def demote(self, client: Client, input: str) -> None:
        pass
    def kick(self, client: Client, input: str) -> None:
        pass
    def kick(self, client: Client, input: str) -> None:
        pass
    def ban(self, client: Client, input: str) -> None:
        pass
    def unban(self, client: Client, input: str) -> None:
        pass
    def mute(self, client: Client, input: str) -> None:
        pass
    def unmute(self, client: Client, input: str) -> None:
        pass
    def create(self, client: Client, input: str) -> None:
        pass
    def delete(self, client: Client, input: str) -> None:
        pass
    def join(self, client: Client, input: str) -> None:
        pass
    def leave(self, client: Client, input: str) -> None:
        pass

## Input Handling ##
    def cmd(self, input: str, client: Client) -> None:
        commands = {'nick': self.nick, 'msg':self.msg, 'names':self.names, 'info':self.client_info, 'info-network':self.client_info_net,
                    'info-server':self.server_info, 'info-channel': self.channel_info, 'quit': self.quit, 'channel-list': self.channel_list,
                    'promote': self.promote, 'demote':self.demote, 'kick':self.kick, 'ban':self.ban, 'unban':self.unban, 'mute':self.mute,
                    'unmute':self.unmute, 'join': self.join, 'leave': self.leave, 'create': self.create, 'delete': self.delete}

        if input[0] == "/":
            cmd = input[1:].split()[0]
            if cmd in commands:
                commands[cmd](client, ' '.join(input[(len(cmd)+1):].split()))
            else:
                client.msg("[server] invalid command")
        else:
            client.msg("[server] invalid command")

## Command Usage ##
    # shows usage for /nick command
    def usage_nick(self, client: Client) -> None:
        client.msg("[server] usage: /nick <new_name>")
        client.msg("[server] <new_name> must be unique, can't be empty, can't contain spaces or tabs")
    # shows usage for /msg command
    def usage_msg(self, client: Client) -> None:
        client.msg("[server] usage: /msg <channel> <message>")
    # shows usage for /info command
    def usage_info(self, client: Client) -> None:
        client.msg("[server] usage: /info")
        client.msg("[server] usage: /info-net               or   /info-network")
        client.msg("[server] usage: /info-server            or   /info-server")
        client.msg("[server] usage: /info-chan <channel>    or   /info-channel <channel>")
    # shows usage for /channel-list command
    def usage_channel(self, client: Client) -> None:
        client.msg("[server] usage: /channel-list")
        client.msg("[server] usage: /create <channel>")
        client.msg("[server] usage: /join <channel>")
        client.msg("[server] usage: /leave <channel>")
        client.msg("[server] You have to be an admin of the channel to use the following commands:")
        client.msg("[server] usage: /promote <channel> <client>")
        client.msg("[server] usage: /demote <channel> <client>")
        client.msg("[server] usage: /kick <channel> <client>")
    # shows usage for /promote command
    def usage_promote(self, client: Client) -> None:
        client.msg("[server] usage: /promote <channel> <client>")

##  Communication  ##
    # sends a message to all clients on a channel
    def msg(self, client: Client, data: str) -> None:
        channel_name = data.split()[0]
        message = " ".join(data.split()[1:])
        if not message:
            self.usage_msg(client)
            return
        if channel_name in self.get_channels_name():
            channel = self.channel_by_name(channel_name)
            if client not in channel.get_clients():
                channel.add_client(client)
        else:
            self.add_channel_create(channel_name, client)
            channel = self.channel_by_name(channel_name)
        message = "[" + channel.get_name() + "] [" + client.get_name() + "] " + message
        channel.broadcast(message)
    # server sends a message to every client on the server
    def broadcast(self, message: str) -> None:
        msg = "[server] " + message
        for client in self.clients:
            client.msg(msg)
    # show log information
    def log(self, message: str) -> None:
        print(message)

## information ##
     # shows client's details
    def client_info(self, client: Client, input: str) -> None:
        client.msg("[client:name] " + client.get_name())
        msg_channels = "[client:channels] " + self.channels_name_by_client_formatted(client)
        client.msg(msg_channels)
    # shows the client's network information
    def client_info_net(self, client: Client, input: str) -> None:
        client.msg("[client:socket] " + str(client.get_socket()))
        client.msg("[client:address] " + client.get_address())
        client.msg("[client:port] " + str(client.get_port()))
    # shows the server's information
    def server_info(self, client: Client, input: str) -> None:
        client.msg("[server:name] " + self.name)
        client.msg("[server:host] " + self.get_host_formatted())
        client.msg("[server:port] " + str(self.port))
        client.msg("[server:clients] " + self.get_clients_name_formatted())
        client.msg("[server:channels] " + self.get_channels_name_formatted())
    # shows a channel's information
    def channel_info(self, client: Client, channel_name: str) -> None:
        channel_name = channel_name.strip()
        if channel_name == "":
            self.usage_info(client)
            return
        if channel_name in self.get_channels_name():
            channel = self.channel_by_name(channel_name)
            client.msg("[channel:name] " + channel.get_name())
            client.msg("[channel:owner] " + channel.get_owner().get_name())
            client.msg("[channel:admins] " + channel.get_admins_name_formatted())
            client.msg("[channel:clients] " + channel.get_clients_name_formatted())
            client.msg("[channel:capacity] " + str(channel.get_capacity()))