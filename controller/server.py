import json
from model.database import DataBase, Tabela


class Server():
    def __init__(self):
        print("Servidor instanciado")

    def salvar_dados(self, data):
        try:
            db = self.setup_db_connection("server")
            r1 = self.__commit_to_db__(db, 'LAUDOS', 'numero_laudo', data)

        except:
            return json.dumps({"Resposta": "Não foi possível salvar as informações no banco de dados"})

        try:
            db_client = self.setup_db_connection("client")
            r2 = self.__commit_to_db__(db_client, 'LAUDOS_REPLICADOS', 'numero_laudo', data)

            return json.dumps({
                "Resposta": "Sucesso ao salvar dados na nuvem e realizar a replicação",
                "Resposta Nuvem": r1,
                "Resposta local": r2
            })

        except:
            # Todo: colocar trativa para desfazer a transação anerior
            return json.dumps({"Resposta": "Não foi possível replicar as informações no banco de dados local"})

    # inicia conexão com banco de dados aws
    def setup_db_connection(self, profile):
        db = DataBase(profile)
        return db

    # salva as informacoes no banco de dados e tabela especificadas
    def __commit_to_db__(self, db, tabela, chave, data):
        table = Tabela(tabela, chave, db) #acessa recurso da tabela
        return table.create(data)
