
import sys
import socket

from flask import Flask
from flask_restful import Resource, Api

from controller.client import Client
from controller.server import Server
from controller.api import *

app = Flask(__name__)
api = Api(app)

api.add_resource(Index, '/')
api.add_resource(Cadastro, '/cadastro')

# identifica host do servidor e solicita que o client informe o host com o qual deseja se conectar
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
        app.run(host=get_host(), debug=True)

    elif sys.argv[1] == 'client':
        client = Client(get_host())
        dados = client.busca_dados()
        client.envia_dados(dados, s)

    else:
        help(0)
