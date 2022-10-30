#!/usr/bin/env python3
import socket
import sys
import select

from tcp_client import *
from tcp_channel import *
from tcp_server import *

def irc_chat(host = "", port = 7777):
    server = Server(host, port)

    while True:
        read, write, error = select.select(server.get_all_sockets(), [], [])
        for socket in read:
            if socket == server.get_socket():
                client_socket, address = socket.accept()
                new_client = Client(client_socket, address)
                server.add_client(new_client)
                server.broadcast(new_client.get_name() + " has joined the server")
                server.log("client [" + new_client.get_name() + "] connected")
            else:
                input = socket.recv(1024).decode("utf-8")
                client = server.client_by_socket(socket)
                if not input or input == "\n" or input == "":
                    server.quit(client, input)
                else:
                    server.cmd(input, client)

def main():
    if len(sys.argv) == 3:
        irc_chat(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 2:
        irc_chat(sys.argv[1])
    else:
        irc_chat()
    return 0

if __name__ == "__main__":
    exit(main())
