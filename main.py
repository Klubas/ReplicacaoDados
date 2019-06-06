
import sys
import socket


from controller.client import Client
from controller.server import Server


#identifica host do servidor e solicita que o client informe o host com o qual deseja se conectar
def get_host():
    if sys.argv[1] == 'client':
        return input("Informe o endereço IP do servidor: ").split(":")
    else:
        return socket.gethostbyname(socket.gethostname())


def help(err):
    print("Use os argumentos [client] ou [server] seguidos da porta usada para conexão [port]")
    print(__file__ + " [client/server] [port]")

    if err < 0:
        print("Erro: " + str(err))

    print("\nArgumentos utilizados: \n")
    print(sys.argv)

    sys.exit(err)


if __name__ == '__main__':
    if sys.argv[1] == 'server':
        server = Server(get_host(), sys.argv[2])
        c = server.inicia_escuta_e_transmissao()
        server.finalizar_conexao(c)

    elif sys.argv[1] == 'client':
        client = Client(get_host())
        dados = client.busca_dados()
        s = client.abre_conexao()
        client.envia_dados(dados, s)
        client.fechar_conexao(s)

    else:
        help(0)
