import json
from requests import put, get, post

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
        dic = {
            "numero_laudo": num_laudo,
            "descricao": descricao
        }
        print(json.dumps(dic))
        return json.dumps(dic)


    def envia_dados(self, message):
        r = put('http://' + self.host + ':' + str(self.port) +  '/cadastro', data=message).json()
        print(r)