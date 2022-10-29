#!/usr/bin/env python3
from ctypes import addressof
import socket
import sys
import select

from tcp_client import *
from tcp_channel import *
from tcp_server import *

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

def irc_chat(host = "", port = 7777):
    s = server(host, port)

    while True:
        read, write, error = select.select(s.all_sockets(), [], [])
        for sock in read:
            if sock == s.socket:
                client_socket, addr = s.socket.accept()
                new_client = client(client_socket, addr)
                s.add_client_copy(new_client)
                s.broadcast(new_client.name + " has joined the server")
                s.log("client [" + new_client.name + "] connected")
            else:
                data = sock.recv(1024).decode("utf-8")
                current_client = s.client_by_socket(sock)
                if not data or data == "\n" or data == "":
                    s.quit(current_client)
                else:
                    s.cmd(data, current_client)

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
