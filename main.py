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
https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html
https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html

"""

import sys
import socket

from model.database import DataBase, Tabela


def client():
    server_addres = get_host()
    host = server_addres[0]

    try:
        port = int(server_addres[1])
    except IndexError:
        port = int(sys.argv[2])

    print("Host: " + host + ":" + str(port))

    s = socket.socket()
    s.connect((host, port))

    num_laudo = input("Num laudo: ")
    descricao = input("Descricao: ")

    message = "numero_laudo: " + num_laudo + "," + "descricao: " + descricao

    #while message != 'q':
    try:
        s.send(message.encode('utf-8'))
        data = s.recv(1024).decode('utf-8')
        print('Received from server: ' + data)
        #message = input('==> ')
    except KeyboardInterrupt:
        print("Conexão Encerrada\n")
    s.close()


def server():

    #inicia conexão com o banco de dados do server
    db = setup_db_connection("server")

    host = get_host()
    port = int(sys.argv[2])

    print("Host: " + host + ":" + str(port))

    s = socket.socket()
    s.bind((host, port))

    s.listen(1)
    c, addr = s.accept()

    print("Connection from: " + str(addr))

    #while True:
    data = c.recv(1024).decode('utf-8')

    if not data:
        #break
        c.close()

    commit_to_db(db, 'LAUDOS', 'numero_laudo', data)

    commit_to_client_db(db, c, data)

    c.close()


def setup_db_connection(profile):
    db = DataBase(profile)
    tables = db.listar_tabelas()
    print(tables)
    return db


def commit_to_db(db, tabela, chave, data):
    print('Dados a serem salvos: ' + data)
    table = Tabela(tabela, chave, db) #acessa recurso da tabela
    return table.create(data)


def commit_to_client_db(db ,c, data):
    c.send(data.encode('utf-8'))


def get_host():
    if sys.argv[1] == 'client':
        return input("Informe o endereço IP do servidor: ").split(":")
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
        #try:
        server()
        #except Exception:
        #    help(-1)
    elif sys.argv[1] == 'client':
        #try:
        client()
        #except Exception:
        #help(-2)
    else:
        help(0)
