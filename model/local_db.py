from pymongo import MongoClient


class LocalDB:
    def __init__(self, host="localhost", port=27017):
        self.host = host
        self.port = port
        self.client = MongoClient(self.host, self.port)
        self.client_db = self.client['LocalDB']

class LocalTable:
    def __init__(self, table, db):
        self.table = db.client_db[table]

    def create(self, documento):
        return self.table.insert_one(documento).inserted_id

    def find(self, filter=None):
        return self.table.find_one(filter)
