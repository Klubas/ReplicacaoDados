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
    print("Use os argumentos [client] ou [server] seguidos do host no formato [host]:[port]")
    print(__file__ + " [client/server] [host]:[port]")

    if err < 0:
        print("Erro: " + str(err))

    print("\nArgumentos utilizados: \n")
    print(sys.argv)

    sys.exit(err)


if __name__ == '__main__':

    if len(sys.argv) == 1:
        app.run(debug=True)
    elif len(sys.argv) == 3:
        hostname=sys.argv[1].split(":")
        host=hostname[0]
        port=hostname[1]
        func=sys.argv[2]
    elif len(sys.argv) == 2:
        hostname=sys.argv[1].split(":")
        host=hostname[0]
        port=hostname[1]
        func="server"
    else:
        help(0)

    if func == 'server':

        app.run(host=host, port=port, debug=True)

    elif func == 'client':

        count = 0
        while True:
            client = Client(host=host, port=port)
            response = json.loads(client.testar_conexao())
            if response['Status'] != 'OK':
                print("Falha na conexão")
                count = count + 1
                if count == 10:
                    print("Todas as tentativas de conexão falharam")
                    exit(-10)
            else:
                break

        while True:
            print("\nInforme os dados do laudo: ")
            dados = client.solicita_dados()
            resposta = client.envia_dados(dados)
            print(resposta)

    else:
        help(0)
