from socket import *

sock = socket(AF_INET, SOCK_STREAM)

host = ''
port = 10000
sock.bind((host, port))

sock.listen(2)
print('aguardando conexão')

while True:
    conn, ender = sock.accept()
    print('conectado no endereço')
    while True:
        data = conn.recv(1024)
        print('recebeu: '+ data.decode())
        if not data: break

        dado_env = input('Digite o que enviar: ')
        conn.send(dado_env.encode())
    conn.close()
