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

from model.database import DataBase


def client():
    server_addres = get_host().split(":")
    host = server_addres[0]

    try:
        port = int(server_addres[1])
    except IndexError:
        port = int(sys.argv[2])

    print("Host: " + host + ":" + str(port))

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
    host = get_host()  # get local machine name
    port = int(sys.argv[2])  # Make sure it's within the > 1024 $$ <65535 range

    print("Host: " + host + ":" + str(port))

    s = socket.socket()
    s.bind((host, port))

    s.listen(1)
    c, addr = s.accept()

    print("Connection from: " + str(addr))
    while True:
        data = c.recv(1024).decode('utf-8')
        if not data:
            break

        data = data.upper()

        commit_to_db(data)

        commit_to_client_db(c, data)

    c.close()

def setup_db_connection():
    db = DataBase()
    tabbles = db.tabelas()
    print(tabbles)

def commit_to_db(data):
    print('From online user: ' + data)


def commit_to_client_db(c, data):
    c.send(data.encode('utf-8'))


def get_host():
    if sys.argv[1] == 'client':
        return input("Informe o endereço IP do servidor: ")
    else:
        return socket.gethostbyname(socket.gethostname())


def help(err):
    print("Use os argumentos [client] ou [server] seguidos da porta usada para conexão [port]")
    print(__file__ + " [client/server] [port]")

    if err < 0:
        print("Erro: " + str(err))

    print("\nArgumentos utilizados: \n")
    print(sys.argv)

    sys.exit(err)

if __name__ == '__main__':
    if sys.argv[1] == 'server':
        try:
            server()
        except Exception:
            help(-1)
    elif sys.argv[1] == 'client':
        try:
            client()
        except Exception:
            help(-2)
    else:
        help(0)
