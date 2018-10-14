from server import app
import server.data as d
from flask import Flask
from flask_restful import reqparse, Api, Resource


api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('task')

class Data(Resource):
    def get(self):
        return d.getData()

    def post(self):
        return d.getData(), 201

api.add_resource(Data, '/features')

