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
        num_laudo = input("Num laudo: ")
        descricao = input("Descricao: ")

        return "numero_laudo: " + num_laudo + "," + "descricao: " + descricao

    def envia_dados(self, message, socket):
        put('http://localhost:5000/cadastro', data=message).json()
        try:
            socket.send(message.encode('utf-8'))
        except KeyboardInterrupt:
            print("Conexão Encerrada\n")