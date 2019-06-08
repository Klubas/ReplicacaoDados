from flask import request
from flask_restful import Resource

from controller.server import Server


class Index(Resource):
    def get(self):
        return {'Status': 'OK'}, 200


class Cadastro(Resource):
    def __init__(self):
        self.server = Server()

    def get(self):
        return {'Status': 'OK'}, 200

    def put(self):
        json = request.get_json(force=True)
        r = self.server.salvar_dados(data=json)
        return {'Status': r}, 201

