import socket
import pickle
import json
from DTO.cardDTO import CardDTO, CardEncoder
from DTO.SolitaireDTO import SolitaireDTO, SolitaireEncoder

# Kilde: https://pythonprogramming.net/pickle-objects-sockets-tutorial-python-3/'
# https://stackoverflow.com/questions/4185242/communication-between-python-client-and-java-server

HOST = "localhost"
PORT = 8080

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

card = CardDTO('C', 3)
print(card)

solitaire = SolitaireDTO(card, ['placeholder', 'placeholder2'], {'C': card, 'D': CardDTO('D', 5)})
print(solitaire)

#data = json.dumps(card, cls=CardEncoder)
data1 = json.dumps(solitaire, cls=SolitaireEncoder)

#sock.sendall(bytes(data, encoding='utf8'))
sock.sendall(bytes(data1, encoding='utf-8'))

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
