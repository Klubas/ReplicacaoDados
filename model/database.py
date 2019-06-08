import boto3
import json
from boto3.dynamodb.conditions import Key


"""
Precisa ter esse arquivo no diretório $HOME com as credenciais AWS
~/.aws/config

[default]
access_key=
secret_key=
region=sa-east-1

[profile client]
aws_access_key_id=
aws_secret_access_key=
region=sa-east-1

[profile server]
aws_access_key_id=
aws_secret_access_key=
region=sa-east-1

"""


class DataBase:
    def __init__(self, profile="default"):
        self.session = boto3.Session(profile_name=profile)
        self.client = self.session.client('dynamodb')
        self.resource = self.session.resource('dynamodb')

    def listar_tabelas(self):
        return self.client.list_tables()['TableNames']


class Tabela:
    def __init__(self, nome, key, db):
        self.db = db
        self.key_name = key
        self.table = self.db.resource.Table(nome)

    def create(self, data_json):
        """
        Grava um registro no banco de dados
        """
        data_json = json.dumps(data_json)
        try:
            if len(self.__query__(data_json['numero_laudo'])['Items']) == 0:  # testa se o item ja existe no banco
                response = self.table.put_item(
                    Item={
                        'numero_laudo': data_json['numero_laudo'],
                        'descricao': data_json['descricao']
                    }
                )
                return response
            else:
                return -2
        except Exception:
            return -1

    def __query__(self, arg):
        try:
            return self.table.query(KeyConditionExpression=Key(self.key_name).eq(arg))
        except TypeError:
            return -1


"""
Não funcional

    def update(self, data):
        data = self.__tratar_dados__(data)

        try:
            response = self.table.update_item(
                Key={self.key_name: data},
                UpdateExpression='SET ' + data[0][0] + ' = :val1 , ' + data[1][0] + ' = :val2',
                ExpressionAttributeValues={
                    ':val1': data[0][1],
                    ':val2': data[1][1]
                }
            )
            return response
        except Exception:
            return -1

    def delete(self, arg):
        try:
            response = self.table.delete_item(
                Key={
                    self.key_name: arg
                }
            )
            return response
        except Exception:
            return -1
"""



