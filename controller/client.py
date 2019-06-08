import json
from requests import put, get


class Client:
    def __init__(self, host="localhost", port=5000):
        self.host = host
        self.port = port

        print("Host: " + self.host + ":" + str(self.port))

    # dados que serão enviados para o servidor
    def solicita_dados(self):
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

        return put(url, data=message, headers=headers).json()

    def testar_conexao(self):
        url = 'http://' + self.host + ':' + str(self.port) + '/'
        res = get(url, timeout=20).json()
        return json.dumps(res)
