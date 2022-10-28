#!/usr/bin/env python3
from ctypes import addressof
import socket
import sys
import select

from tcp_client import *
from tcp_channel import *
from tcp_server import *

# def handle_cmd(line, l, s, sock, dict):
#     cmd = line.split(" ", 1)[0]
#     if cmd == "MSG":
#         msg = line.split("MSG ", 1)[1]
#         MSG(msg, l, s, sock, dict)
#     elif cmd == "NICK":
#         NICK(line, sock, dict)
#     elif cmd == "NAMES\n":
#         NAMES(sock, dict)
#     elif cmd == "QUIT":
#         quit = line.split("QUIT ", 1)[1]
#         MSG(quit, l, s, sock, dict)
#         LEAVE(sock, l, s, dict)
#     elif cmd == "KILL":
#         KILL(l, s, sock, dict, line)
#     else:
#         INVALID(sock)
# def INVALID(socket):
#     socket.sendall("Invalid command\n".encode("utf-8"))
# def NICK(line, sock, dict):
#     nick = line.split("NICK ", 1)[1]
#     nick = nick[:-1]
#     for key in dict:
#         if dict[key] == nick:
#             sock.sendall("Nickname already taken\n".encode("utf-8"))
#             return
#     print("client [", dict[sock], "] => [", nick, "]", sep='')
#     dict[sock] = nick
# def NAMES(sock, dict):
#     name_list = "[server] "
#     for key in dict:
#         if (dict[key] != "server"):
#             name_list += str(dict[key])
#             name_list += ', '
#     name_list = name_list[:-2]
#     name_list += '\n'
#     sock.sendall(name_list.encode("utf-8"))
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
                s.broadcast(new_client.name + " has joined the chat\n")
                s.log("client [" + new_client.name + "] connected")
            else:
                data = sock.recv(1024)
                if not data or data.decode("utf-8") == "\n" or data.decode("utf-8") == "":
                    s.quit(s.client_by_socket(sock))
                # else:
                #     handle_cmd(data.decode("utf-8"), l, s, sock, dict)

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
