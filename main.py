import sys
import json

from flask import Flask
from flask_restful import Api

from controller.client import Client
from controller.api import Cadastro, Index

app = Flask(__name__)
api = Api(app)

api.add_resource(Index, '/')
api.add_resource(Cadastro, '/cadastro')

# identifica host do servidor e solicita que o client informe o host com o qual deseja se conectar

def help(err):
    print("Use os argumentos [client] ou [server] seguidos da porta usada para conexão [port]")
    print(__file__ + " [client/server] [port]")

    if err < 0:
        print("Erro: " + str(err))

    print("\nArgumentos utilizados: \n")
    print(sys.argv)

    sys.exit(err)


if __name__ == '__main__':
    ip = "192.168.0.104"
    if sys.argv[1] == 'server':

        # ip = input("Informe o endereço do servidor: ")

        app.run(host=ip, port=sys.argv[2], debug=True)

    elif sys.argv[1] == 'client':

        while True:
            ip = input("Informe o endereço do servidor que deseja conectar: ")
            client = Client(host=ip, port=sys.argv[2])
            response = json.loads(client.testar_conexao())
            if response['Status'] != 'OK':
                print("Falha na conexão")
            else:
                break

        while True:
            print("\nInforme os dados do laudo: ")
            dados = client.solicita_dados()
            resposta = client.envia_dados(dados)
            print(resposta)

    else:
        help(0)
