import socket

# Kilde: https://pythonprogramming.net/pickle-objects-sockets-tutorial-python-3/'
# https://stackoverflow.com/questions/4185242/communication-between-python-client-and-java-server
# Siff ravn and Filip Brix Jensen
class Socket:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def send(self, data):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.host, self.port))
        sock.sendall(bytes(data, encoding='utf-8'))
        print("\nData sent")
        sock.close()

    def receive(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.host, self.port))
        data = sock.recv(4096)
        sock.close()
        print("Data received")
        msg = data.decode('utf-8')
        print(msg)
        return msg
