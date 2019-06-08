from model.database import DataBase, Tabela


class Server():
    def __init__(self):
        print("Servidor instanciado")

    def salvar_dados(self, data):
        try:
            db = self.setup_db_connection("server")
            r = self.__commit_to_db__(db, 'LAUDOS', 'numero_laudo', data)
            print(r)
            try: # se tiver sucesso salva no banco do client:
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
        table = Tabela(tabela, chave, db) #acessa recurso da tabela
        table.create(data)
        return "Commit"
