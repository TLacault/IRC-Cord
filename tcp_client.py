#!/usr/bin/env python3
import socket as Socket

class Client:
    def __init__(self, socket: Socket, address: object) -> None:
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
    def get_socket(self) -> Socket:
        return self.socket
    # returns the client's address
    def get_address(self) -> str:
        return self.address
    # returns the client's port
    def get_port(self) -> str:
        return self.port
    # returns a list of all client's friends
    def get_friends(self) -> list[object]:
        return self.friends

## Setters ##
    # sets the client's name
    def set_name(self, name: str) -> None:
        self.name = name
    # sets the client's socket
    def set_socket(self, socket: Socket) -> None:
        self.socket = socket
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

## Search ##
    # search for a friend by name
    def friend_by_name(self, name: str) -> object:
        for friend in self.friends:
            if friend.get_name() == name:
                return friend
        return None
    # search for a friend by socket
    def friend_by_socket(self, socket: Socket) -> object:
        for friend in self.friends:
            if friend.get_socket() == socket:
                return friend
        return None
    # returns a list all common friends with another client
    def common_friends(self, client: object) -> list[object]:
        common = []
        for friend in self.friends:
            if friend in client.get_friends():
                common.append(friend)
        return common

##  Client Management  ##
    # close the client's connection
    def close(self) -> None:
        self.socket.close()

## Communications ##
    # sends a message to the client
    def msg(self, message: str) -> None:
        if message[-1] != '\n':
            message += '\n'
        self.socket.send(message.encode("utf-8"))
    # show log information
    def log(self, message: str) -> None:
        print(message)
