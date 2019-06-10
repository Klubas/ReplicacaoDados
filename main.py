#!/usr/bin/env python
import sys
import json
import docker
from datetime import datetime

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


import netifaces
import ipaddress



# Thanks stackoverflow https://stackoverflow.com/questions/39988525/find-local-non-loopback-ip-address-in-python
def get_local_non_loopback_ipv4_addresses():
    for interface in netifaces.interfaces():
        # Not all interfaces have an IPv4 address:
        if netifaces.AF_INET in netifaces.ifaddresses(interface):
            # Some interfaces have multiple IPv4 addresses:
            for address_info in netifaces.ifaddresses(interface)[netifaces.AF_INET]:
                address_object = ipaddress.IPv4Address((address_info['addr']))
                if not address_object.is_loopback:
                    yield address_info['addr']


if __name__ == '__main__':

    localhost = list(get_local_non_loopback_ipv4_addresses())
    print(localhost)

    if len(sys.argv) == 2:

        func = sys.argv[1]

    else:

        help(-1)

    """
    try:
        hostname = input("\nInforme o endereço do servidor [host:port]: ").split(":")
        host = hostname[0]
        port = hostname[1]
        e = False
        print(hostname)
    except IndexError as ex:
        print("Formato inválido\n")
        exit(-1)
    """

    host = localhost[0]
    port = 5000

    if func == 'server':

        app.run(host=host, port=port, debug=False)

    elif func == 'client':

        #inicia servidor mongodb no docker
        try:
            docker_client = docker.from_env()

            #baixa uma container do mongo
            image = docker_client.images.pull('mongo:latest')
            print(image)
            print("Em caso de erro de permissão execute `docker pull mongo` no terminal")

            container = docker_client.containers.run(
                image="mongo:latest",
                name="ReplicacaoDB",
                ports={'27017/tcp': 27017}
            )

            container.logs()

        except Exception as e:
            print(e)

        hostname = input("\nInforme o endereço do servidor [host:port]: ").split(":")
        try:
            host = hostname[0]
            port = hostname[1]
        except IndexError:
            port = 5000

        print(hostname)


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
            dados["hostname"] = localhost[0]
            dados["date_insert"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            dados = json.dumps(dados)

            resposta = client.envia_dados(dados)
            print(resposta)

    else:
        help(0)
