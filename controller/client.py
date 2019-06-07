from requests import put, get

class Client:
    def __init__(self, server_address):
        self.host = server_address[0]

        try:
            self.port = int(server_address[1])
        except IndexError:
            self.port = int(8080)

        print("Host: " + self.host + ":" + str(self.port))


    def busca_dados(self):
        #dados que serão enviados para o servidor
        return get('http://localhost:5000/cadastro').json()


    def envia_dados(self, message):
        put('http://localhost:5000/cadastro', data=message).json()
