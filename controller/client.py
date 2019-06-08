import json
from requests import put, get, post

class Client:
    def __init__(self, hostname):
        server_address = hostname.split(":")

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
        dic = {
            "numero_laudo": num_laudo,
            "descricao": descricao
        }
        return json.dumps(dic)


    def envia_dados(self, message):

        url = 'http://' + self.host + ':' + str(self.port) + '/cadastro'

        headers = {"Content-Type": "application/json"}

        response = put(url, data=message, headers=headers)

        return response.json()
