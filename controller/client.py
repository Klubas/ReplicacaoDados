import socket

class Client:
    def __init__(self, server_address):
        self.host = server_address[0]

        try:
            self.port = int(server_address[1])
        except IndexError:
            self.port = int(8080)

        print("Host: " + self.host + ":" + str(self.port))

    def abre_conexao(self):
        s = socket.socket()
        s.connect((self.host, self.port))
        return s

    def busca_dados(self):
        #dados que serão enviados para o servidor
        num_laudo = input("Num laudo: ")
        descricao = input("Descricao: ")

        return "numero_laudo: " + num_laudo + "," + "descricao: " + descricao

    def envia_dados(self, message, socket):
        try:
            socket.send(message.encode('utf-8'))
        except KeyboardInterrupt:
            print("Conexão Encerrada\n")

    def fechar_conexao(self, socket):
        socket.close()