import socket
from model.database import DataBase, Tabela

class Server():
    def __init__(self, host, port):

        self.host = host
        self.port = int(port)

        print("Host: " + host + ":" + str(port))

    def inicia_escuta_e_transmissao(self):
        s = socket.socket()
        s.bind((self.host, self.port))

        s.listen(1)
        c, addr = s.accept()

        print("Conexão do endereço: " + str(addr))
        data = c.recv(1024).decode('utf-8')

        if not data:
            c.close()
            return -1
        else:
            self.salvar_dados(data)
            return c

    def finalizar_conexao(self, connection):
        connection.close()

    def salvar_dados(self, data):
        try:
            db = self.setup_db_connection("server")
            r = self.commit_to_db(db, 'LAUDOS', 'numero_laudo', data)
            print(r)
        except:
            print("Não foi possível salvar as informações no banco de dados")
            exit(-1)

        #se tiver sucesso:
        try:
            db_client = self.setup_db_connection("client")
            r = self.commit_to_db(db_client, 'LAUDOS_REPLICADOS', 'numero_laudo', data)
            print(r)
        except:
            print("Não foi possível replicar as informaçõespara o banco de dados client")


    #inicia conexão com banco de dados aws
    def setup_db_connection(self, profile):
        db = DataBase(profile)
        tables = db.listar_tabelas()
        print(tables)
        return db

    #salva as informacoes no banco de dados e tabela especificadas
    def commit_to_db(self, db, tabela, chave, data):
        print('Dados a serem salvos: ' + data)
        table = Tabela(tabela, chave, db) #acessa recurso da tabela
        return table.create(data)
