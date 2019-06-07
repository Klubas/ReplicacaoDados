from model.database import DataBase, Tabela

class Server():
    def __init__(self, host, port):
        self.host = host
        self.port = int(port)
        print("Host: " + host + ":" + str(port))

    def salvar_dados(self, data):
        try:
            db = self.setup_db_connection("server")
            r = self.__commit_to_db__(db, 'LAUDOS', 'numero_laudo', data)
            print(r)
        except:
            print("Não foi possível salvar as informações no banco de dados")
            exit(-1)

        # se tiver sucesso:
        try:
            db_client = self.setup_db_connection("client")
            r = self.__commit_to_db__(db_client, 'LAUDOS_REPLICADOS', 'numero_laudo', data)
            print(r)
        except:
            print("Não foi possível replicar as informaçõespara o banco de dados client")

    # inicia conexão com banco de dados aws
    def setup_db_connection(self, profile):
        db = DataBase(profile)
        tables = db.listar_tabelas()
        print(tables)
        return db

    # salva as informacoes no banco de dados e tabela especificadas
    def __commit_to_db__(self, db, tabela, chave, data):
        print('Dados a serem salvos: ' + data)
        table = Tabela(tabela, chave, db) #acessa recurso da tabela
        return table.create(data)
