from socket import *

sock = socket(AF_INET, SOCK_STREAM)
host = 'localhost'
port = 10000

sock.connect((host, port))
print('cliente conectado')
while True:
    msg = input('digite sua mensagem: ')
    sock.send(msg.encode())
    data_resp = sock.recv(1024)

    print (data_resp.decode())

