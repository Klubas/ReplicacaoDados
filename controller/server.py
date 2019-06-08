from model.database import DataBase, Tabela

class Server():
    def __init__(self):
        pass

    def salvar_dados(self, data):
        db = self.setup_db_connection("server")
        r = self.__commit_to_db__(db, 'LAUDOS', 'numero_laudo', data)
        print(r)
        return r
        try:
            db = self.setup_db_connection("server")
            r = self.__commit_to_db__(db, 'LAUDOS', 'numero_laudo', data)
            print(r)
            try: # se tiver sucesso:
                db_client = self.setup_db_connection("client")
                r = self.__commit_to_db__(db_client, 'LAUDOS_REPLICADOS', 'numero_laudo', data)
                print(r)
            except:
                # Todo: colocar trativa para desfazer a transação anerior
                print("Não foi possível replicar as informações para o banco de dados client")
                return"Erro"
        except:
            print("Não foi possível salvar as informações no banco de dados")
            return("Erro")


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
