import boto3
from boto3.dynamodb.conditions import Attr, Key


class DataBase():
    def __init__(self, profile="default"):
        self.session = boto3.Session(profile_name=profile)
        self.client = self.session.client('dynamodb')
        self.resource = self.session.resource('dynamodb')

    def listar_tabelas(self):
        return self.client.list_tables()['TableNames']


class Tabela():
    def __init__(self, nome, key, db):
        self.db = db
        self.key_name = key
        self.table = self.db.resource.Table(nome)

    def query(self, arg):
        try:
            return self.table.query(KeyConditionExpression=Key(self.key_name).eq(arg))
        except Exception:
            return -1

    def create(self, data):
        data = data.split(",")
        for i in range(0, len(data)):
            data[i] = data[i].split(":")

        #try:
        if len(self.query(data[0][1])['Items']) == 0:  # testa se o item ja existe no banco
            response = self.table.put_item(
                Item={
                    data[0][0]: data[0][1],
                    data[1][0]: data[1][1]
                }
            )
            return response
        else:
            return -2
       # except Exception:
       #     return -1

    def update(self, data):
        try:
            response = self.table.update_item(
                Key={self.key_name: data},
                UpdateExpression='SET username = :val1 , first_name = :val2 , last_name = :val3 , conta = :val4',
                ExpressionAttributeValues={
                    ':val1': data
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

