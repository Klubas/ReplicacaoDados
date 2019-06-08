import json
from requests import put, get

class Client:
    def __init__(self, server_address):
        self.host = server_address[0]

        try:
            self.port = int(server_address[1])
        except IndexError:
            self.port = int(5000)

        print("Host: " + self.host + ":" + str(self.port))


    def busca_dados(self):
        #dados que serão enviados para o servidor
        num_laudo = input("Num laudo: ")
        descricao = input("Descricao: ")
        #dic = 1
        return json.dumps(dic)


    def envia_dados(self, message):
        put('http://localhost:5000/cadastro', data=message).json()
