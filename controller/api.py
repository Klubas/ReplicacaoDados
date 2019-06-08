from flask import request
from flask_restful import Resource, Api

from controller.server import Server


class Index(Resource):
    def get(self):
        return { 'Status': 'OK' }

class Cadastro(Resource):
    def __init__(self):
        self.server = Server()

    def get(self):
        return {'hello': 'world'}

    def put(self):
        json = request.get_json(force=True)
        r = self.server.salvar_dados(data=json)
        return {'Status': r}, 201

