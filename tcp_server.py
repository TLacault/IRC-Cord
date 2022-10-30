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
    # returns a list of all channels the admin is in
    def channels_by_admin(self, admin: Client) -> list:
        channels = [Channel]
        for channel in self.channels:
            if admin in channel.get_admins():
                channels.append(channel)
        return channels

## Commands ##
    # modifies the name of the client if it is not taken
    def nick(self, client: Client, nick: str) -> None:
        nick = nick.replace("\t", "")
        nick = nick.replace("\n", "")
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
    def quit(self, client: Client) -> None:
        self.remove_client(client)
        self.broadcast(client.get_name() + " has left the server")
        self.log("client [" + client.get_name() + "] disconnected")
        client.close()
   # sends a list of all client's name on the server to the client
    def names(self, client: Client) -> str:
        client.msg("[server] " + self.get_clients_name_formatted())


# def KILL(l, s, sock, dict, line):
#     nick = line.split(" ", 2)[1]
#     try:
#         argument = line.split(" ", 2)[2]
#     except:
#         INVALID(sock)
#         return
#     msg = nick + " has been kicked by " + dict[sock] + " : " + argument
#     for key in dict:
#         if dict[key] == nick and key != s and key != sock:
#             print("client [", dict[sock], "] ", "kicked [", dict[key], "]", sep='')
#             MSG(msg, l, s, s, dict)
#             LEAVE(key, l, s, dict)
#             return
#     msg = nick + " not found\n"
#     sock.sendall(msg.encode("utf-8"))


    def cmd(self, input: str, client: Client) -> None:
        if input[0] == '/':
            cmd = input[1:].split(' ')[0]
            cmd = cmd.replace("\n", "")
            if cmd == 'nick':
                self.nick(client, input[6:])
            elif cmd == "msg":
                self.msg(client, input[5:])
            elif cmd == 'names':
                self.names(client)
            elif cmd == 'info':
                self.client_info(client)
            elif cmd == 'info-net':
                self.client_info_net(client)
            elif cmd == 'info-server':
                self.server_info(client)
            elif cmd == 'quit':
                self.quit(client)
            else:
                client.msg("[server] invalid command\n")
        else:
            client.msg("[server] invalid command\n")

## Command Usage ##
    # shows usage for /nick command
    def usage_nick(self, client: Client) -> None:
        client.msg("[server] usage: /nick <new_name>")
        client.msg("[server] <new_name> must be unique, can't be empty, can't contain spaces or tabs")
    # shows usage for /msg command
    def usage_msg(self, client: Client) -> None:
        client.msg("[server] usage: /msg <channel> <message>")

##  Communication  ##
    # sends a message to all clients on a channel #TO DO
    def msg(self, client: Client, data: str) -> None:
        channel_name = data.split(" ")[0]
        if channel_name in self.get_channels_name():
            current_channel = self.channel_by_name(channel_name)
            if client not in current_channel.get_clients():
                current_channel.add_client(client)
        else:
            self.add_channel_create(channel_name, client)
            current_channel = self.channel_by_name(channel_name)
        try:
            message = data.split(" ", 1)[1]
        except IndexError:
            self.usage_msg(client)
            return
        message = message.strip()
        if message == "":
            self.usage_msg(client)
            return
        formatted_message = "[" + current_channel.get_name() + "] [" + client.get_name() + "] " + message
        current_channel.msg_clients(formatted_message)
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
    def client_info(self, client: Client) -> None:
        client.msg("[client:name] " + client.get_name())
        msg_channels = "[client:channels] " + ", ".join(self.channels_by_client(client))
        if msg_channels[-2:] == ", ":
            msg_channels = msg_channels[:-2]
        else:
            msg_channels += "try /channel-help"
        client.msg(msg_channels)
    # shows the client's network information
    def client_info_net(self, client: Client) -> None:
        client.msg("[client:socket] " + str(client.get_socket()))
        client.msg("[client:address] " + client.get_address())
        client.msg("[client:port] " + str(client.get_port()))
    # shows the server's information
    def server_info(self, client: Client) -> None:
        client.msg("[server:name] " + self.name)
        client.msg("[server:host] " + self.get_host_formatted())
        client.msg("[server:port] " + str(self.port))
        client.msg("[server:clients] " + self.get_clients_name_formatted())
        client.msg("[server:channels] " + self.get_channels_name_formatted())