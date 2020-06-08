import socket
import pickle
import json

from DTO.buildingTowerDTO import BuildingTowerDTO
from DTO.cardDTO import CardDTO, CardEncoder
from DTO.SolitaireDTO import SolitaireDTO, SolitaireEncoder


# Kilde: https://pythonprogramming.net/pickle-objects-sockets-tutorial-python-3/'
# https://stackoverflow.com/questions/4185242/communication-between-python-client-and-java-server

class Socket:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def send(self, data):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.host, self.port))
        sock.sendall(bytes(data, encoding='utf-8'))


# sock.sendall(b'Hello\r\n')
# data = sock.recv(1024)
# print ("1)", data)
#
# if ( data == b'olleH\r\n'):
#     sock.sendall(b'Bye\n')
#     data = sock.recv(1024)
#     print ("2)", data)
#
#     if (data == b'eyB\r\n'):
#         sock.close()
#         print ("Socket closed")
