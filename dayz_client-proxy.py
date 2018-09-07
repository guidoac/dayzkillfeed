from socket import *

class Cliente():
    def __init__(self, host, port):
        sock_main = socket(AF_INET, SOCK_STREAM)
        sock_main.bind((host,port))
        sock_main.listen(5)
