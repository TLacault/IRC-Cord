#!/usr/bin/env python3
from ctypes import addressof
import socket
import sys
import select

from tcp_client import *
from tcp_channel import *
from tcp_server import *

def tcp_select(host = "", port = 7777):
    s = server(host, port)
    s.show()
    return

def main():
    if len(sys.argv) == 3:
        tcp_select(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 2:
        tcp_select(sys.argv[1])
    else:
        tcp_select()
    return 0

if __name__ == "__main__":
    exit(main())
