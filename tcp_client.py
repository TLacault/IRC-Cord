#!/usr/bin/env python3
from ctypes import addressof
import socket
import sys
import select

class client:
    def __init__(self: object, socket: object, address: object) -> None:
        self.socket = socket
        self.address = str(address[0])
        self.port = str(address[1])
        self.name = self.address + ':' + self.port
        self.friends = []

## Getters ##
    # returns the client's name
    def get_name(self) -> str:
        return self.name
    # returns the client's socket
    def get_socket(self) -> object:
        return self.socket
    # returns the client's address
    def get_address(self) -> str:
        return self.address
    # returns the client's port
    def get_port(self) -> str:
        return self.port
    # returns a list of all client's friends
    def get_friends(self) -> list:
        return self.friends

## Setters ##
    # sets the client's name
    def set_name(self, name: str) -> None:
        self.name = name
    # sets the client's socket
    def set_socket(self, sock: object) -> None:
        self.socket = sock
    # sets the client's address
    def set_address(self, addr: str) -> None:
        self.address = addr
    # sets the client's port
    def set_port(self, port: str) -> None:
        self.port = port
    # sets the client's friends list
    def set_friends(self, friends: list) -> None:
        self.friends = friends

## Modifiers ##
    # add a friend to the client's friend list
    def add_friend(self, friend: object) -> bool:
        if friend not in self.friends:
            self.friends.append(friend)
            return True
        return False
    # remove a friend from the client's friend list
    def remove_friend(self, friend: object) -> bool:
        if friend in self.friends:
            self.friends.remove(friend)
            return True
        return False

##  Client Management  ##
    # close the client's connection
    def close(self) -> None:
        self.socket.close()

## Command Usage ##
    # shows usage for /nick command
    def usage_nick(self) -> None:
        self.msg("[server] usage: /nick <new_name>")
        self.msg("[server] <new_name> must be unique, can't be empty, can't contain spaces or tabs")

## Communications ##
    # sends a message to the client
    def msg(self, message: str) -> None:
        if message[-1] != '\n':
            message += '\n'
        self.socket.send(message.encode("utf-8"))
    # show log information
    def log(self, message) -> None:
        print(message)
