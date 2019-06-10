import os
import json
from model.database import DataBase, TabelaLaudos
from model.local_db import LocalDB, LocalTable


class Server:
    def __init__(self):
        print("Servidor instanciado")

    def salvar_dados(self, data):
        try:
            print(os.environ['KEY_ID'] + " - " + os.environ['SECRET_KEY'])
            db = self.setup_db_connection(key_id=os.environ['KEY_ID'], secret_key=os.environ['SECRET_KEY'])
            table = self.__acessar_recurso_tabela('LAUDOS', 'numero_laudo', db)
            r1 = self.__commit_to_db__(table, data)
            try:
                print("LocalDB ADDR = " + data['hostname'] + ":" + str(27017))
                db_client = self.setup_local_db_connection(host=data['hostname'], port=27017)
                local_table = self.__acessar_recurso_tabela_local('LAUDOS', db_client)
                r2 = self.__commit_to_local_db(local_table, data)
                return json.dumps({
                    "Resposta Nuvem": r1,
                    "Resposta local": str(r2)
                })

            except Exception as e:
                # Trativa para desfazer a transação anterior caso queira manter consistencia entre as duas bases
                try:
                    print(data[table.key_name])
                    r3 = self.__delete_from_db(table, data[table.key_name])
                except Exception as delete_exception:
                    print(delete_exception)
                    r3 = "Não foi possível desfazer a transação"
                print(e)
                return json.dumps({"Resposta": "Não foi possível replicar as informações no banco de dados local", "Transacao": r3})
        except Exception as e:
            print(e)
            return json.dumps({"Resposta": "Não foi possível salvar as informações no banco de dados"})

    # inicia conexão com banco de dados

    def setup_db_connection(self, key_id=None, secret_key=None):
        return DataBase(key_id, secret_key)

    def __acessar_recurso_tabela(self, nome_tabela, chave, db):
        return TabelaLaudos(nome_tabela, chave, db)  # acessa recurso da tabela

    def setup_local_db_connection(self, host=None, port=None):
        return LocalDB(host, port)

    def __acessar_recurso_tabela_local(self, nome_tabela, db):
        return LocalTable(nome_tabela, db)

    # salva as informacoes no banco de dados e tabela especificadas

    def __commit_to_db__(self, table, data):
        return table.create(data)

    def __delete_from_db(self, table, valor_chave):
        return table.delete(valor_chave)

    def __commit_to_local_db(self, table, documento):
        return table.create(documento)