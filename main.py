"""

Comunicação entre duas aplicações cliente servidor

Cliente
 - Recebe os dados
 - Envia para o servidor

Servidor
 - Recebe os dados do cliente
 - Salva os dados do cliente
 - Envia os dados salvos de volta para o cliente

Cliente
 - Recebe os dados do servidor
 - Salva os dados do servidor

Referências
https://medium.com/podiihq/networking-how-to-communicate-between-two-python-programs-abd58b97390a

"""

import sys
import socket


def client():
    host = socket.gethostname()  # get local machine name
    port = 8080  # Make sure it's within the > 1024 $$ <65535 range

    s = socket.socket()
    s.connect((host, port))

    message = input('-> ')
    while message != 'q':
        s.send(message.encode('utf-8'))
        data = s.recv(1024).decode('utf-8')
        print('Received from server: ' + data)
        message = input('==> ')
    s.close()


def server():
    host = socket.gethostname()  # get local machine name
    port = 8080  # Make sure it's within the > 1024 $$ <65535 range

    s = socket.socket()
    s.bind((host, port))

    s.listen(1)
    c, addr = s.accept()
    print("Connection from: " + str(addr))
    while True:
        data = c.recv(1024).decode('utf-8')
        if not data:
            break
        print('From online user: ' + data)
        data = data.upper()
        c.send(data.encode('utf-8'))

    c.close()


if __name__ == '__main__':
    if sys.argv[1] == 'server':
        server()
    elif sys.argv[1] == 'client':
        client()
    else:
        print("Use os argumentos [client] ou [server]")
        sys.exit(-1)
