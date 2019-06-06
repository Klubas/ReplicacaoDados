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

    #dados que serão enviados para o servidor
    num_laudo = input("Num laudo: ")
    descricao = input("Descricao: ")

    message = "numero_laudo: " + num_laudo + "," + "descricao: " + descricao

    try:
        s.send(message.encode('utf-8'))
    except KeyboardInterrupt:
        print("Conexão Encerrada\n")
    s.close()


def server():

    host = get_host()
    port = int(sys.argv[2])

    print("Host: " + host + ":" + str(port))

    s = socket.socket()
    s.bind((host, port))

    s.listen(1)
    c, addr = s.accept()

    print("Connection from: " + str(addr))

    data = c.recv(1024).decode('utf-8')

    if not data:
        c.close()

    salvar_dados(data)

    c.close()

def salvar_dados(data):
    try:
        db = setup_db_connection("server")
        r = commit_to_db(db, 'LAUDOaS', 'numero_laudo', data)
        print(r)
    except:
        print("Não foi possível salvar as informações no banco de dados")
        exit(-1)

    # se tiver sucesso:
    try:
        db_client = setup_db_connection("client")
        r = commit_to_db(db_client, 'LAUDOS_REPLICADOS', 'numero_laudo', data)
        print(r)
    except:
        print("Não foi possível replicar as informaçõespara o banco de dados client")


#inicia conexão com banco de dados aws
def setup_db_connection(profile):
    db = DataBase(profile)
    tables = db.listar_tabelas()
    print(tables)
    return db


def commit_to_db(db, tabela, chave, data):
    print('Dados a serem salvos: ' + data)
    table = Tabela(tabela, chave, db) #acessa recurso da tabela
    return table.create(data)


#identifica host do servidor e solicita que o client informe o host com o qual deseja se conectar
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
        server()
    elif sys.argv[1] == 'client':
        client()
    else:
        help(0)
