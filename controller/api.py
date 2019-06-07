from flask import request
from flask_restful import Resource, Api

class Index(Resource):
    def get(self):
        return { 'Status': 'OK' }

class Cadastro(Resource):
    def get(self):
        return {'hello': 'world'}

    def post(self):
        json = request.get_json()
        return {'Sent': json}, 201

