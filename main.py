import sys
import json
import docker
import socket

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
    print("Use os argumentos [client] ou [server]")
    print(__file__ + " [client/server]")

    if err < 0:
        print("Erro: " + str(err))

    print("\nArgumentos utilizados: \n")
    print(sys.argv)

    sys.exit(err)


if __name__ == '__main__':

    if len(sys.argv) == 2:

        func = sys.argv[1]

    else:

        help(-1)

    try:
        hostname = input("\nInforme o endereço do servidor [host:port]: ").split(":")
        host = hostname[0]
        port = hostname[1]
        e = False
        print(hostname)
    except IndexError as ex:
        print("Formato inválido\n")
        exit(-1)

    if func == 'server':

        app.run(host=host, port=port, debug=True)

    elif func == 'client':

        #inicia servidor mongodb no docker
        try:
            docker_client = docker.from_env()

            #baixa uma container do mongo
            image = docker_client.images.pull('mongo:latest')
            print(image)

            container = docker_client.containers.run(
                image="mongo:latest",
                name="ReplicacaoDB",
                ports={'27017/tcp': 27017}
            )

            container.logs()

        except Exception as e:
            print(e)

        count = 0
        while True:

            client = Client(host, port)

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

            dados = json.loads(dados)
            dados["hostname"] = socket.gethostbyname(socket.gethostname())
            dados = json.dumps(dados)

            resposta = client.envia_dados(dados)
            print(resposta)

    else:
        help(0)
