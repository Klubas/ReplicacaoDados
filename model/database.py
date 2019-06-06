import boto3
from boto3.dynamodb.conditions import Attr, Key

class DataBase():
    def __init__(self):
        self.resource = boto3.resource('dynamodb')
        self.client = boto3.client('dynamodb')

    def tabelas(self):
        return self.client.list_tables()['TableNames']


class Tabela():
    def __init__(self, nome, key, db):
        self.db = db
        self.table = self.db.resource.Table(nome)
        self.key_name = key

    def query(self, arg):
        try:
            return self.table.query(KeyConditionExpression=Key(self.key_name).eq(arg))
        except Exception:
            return -1

    def scan_ne(self, arg1, arg2):
        try:
            return self.table.scan(FilterExpression=Attr(arg1).ne(arg2))
        except Exception:
            return -1

    def query_data_table(self, arg):
        tmp_user = User()
        resposta = self.query(arg)  # Dicionario com todos os dados do banco/tabela/usuario
        if resposta != -1:
            if len(resposta) > 0:
                user = resposta['Items'][0]
                tmp_user.email = user['email']
                tmp_user.username = user['username']
                tmp_user.first_name = user['first_name']
                tmp_user.last_name = user['last_name']
                tmp_user.conta = user['conta']
        return tmp_user

    def create(self, user):
        try:
            if len(self.query(user.email)['Items']) == 0:  # testa se o item ja existe no banco
                response = self.table.put_item(
                    Item={
                        'email': user.email,
                        'username': user.username,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'conta': user.conta
                    }
                )
                return response
            else:
                return -2
        except Exception:
            return -1

    """
    {
        TableName: "Music",
        Item: {
            "Artist":"No One You Know",
            "SongTitle":"Call Me Today",
            "AlbumTitle":"Somewhat Famous",
            "Year": 2015,
            "Price": 2.14,
            "Genre": "Country",
            "Tags": {
                "Composers": [
                    "Smith",
                    "Jones",
                    "Davis"
                ],
                "LengthInSeconds": 214
            }
        }
    }
    """

    def update(self, user):
        try:
            response = self.table.update_item(
                Key={self.key_name: user.email},
                UpdateExpression='SET username = :val1 , first_name = :val2 , last_name = :val3 , conta = :val4',
                ExpressionAttributeValues={
                    ':val1': user.username,
                    ':val2': user.first_name,
                    ':val3': user.last_name,
                    ':val4': user.conta
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

