import flask
from flask import Flask, jsonify
from flask_restful import reqparse, abort, Api, Resource
from flask import request
from flask_restful import Resource
from data import db_session
from db.local_db_api import *

app = Flask(__name__)
api = Api(app)
dbm = DataBaseManager()


parser = reqparse.RequestParser()
# parser - это prorerties
parser.add_argument('login', required=False, location='args')
parser.add_argument('password', required=False, location='args')


class UserAuth(Resource):
    def get(self):
        args = parser.parse_args()
        print(args)
        if dbm.entrance_user(args.login, args.password):
            response = jsonify({'result': 'ok'})
        else:
            response = jsonify({'result': 'not ok'})
            response.status_code = 404
        return jsonify({'user_id': 1, 'user_name': 'Vasya'})


class UserRegistration(Resource):
    def post(self):
        json_data = request.get_json()


class NewsResource(Resource):
    def get(self):
        return jsonify({
            'news':
                []
            }
        )
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('title', required=True)
        parser.add_argument('content', required=True)
        parser.add_argument('user_id', required=True, type=int)
        args = parser.parse_args()
        return jsonify({'id': id})


db_session.global_init("db/blogs.db")
api.add_resource(UserAuth, '/user/registration')
api.add_resource(NewsResource, '/')
app.run()

#http://127.0.0.1:5000/4?title=werty&content=werty&user_id=234
