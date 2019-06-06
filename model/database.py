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



    def create(self, data):
        data = self.__tratar_dados__(data)

        #try:
        if len(self.__query__(data[0][1])['Items']) == 0:  # testa se o item ja existe no banco
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
        modelo dos dados:
    {
        numero_laudo: valor, 
        descricao: desc'
    }   
    """

    def __tratar_dados__(self, data):
        data = data.split(",")
        for i in range(0, len(data)):
            data[i] = data[i].split(":")
        return data

    def __query__(self, arg):
        try:
            return self.table.query(KeyConditionExpression=Key(self.key_name).eq(arg))
        except Exception:
            return -1

