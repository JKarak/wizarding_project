import flask
import werkzeug
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
        return response


class UserRegistration(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        login = json_data['login']
        key = json_data['key']
        email = json_data['email']
        if dbm.add_user(login, key, email):
            response = jsonify({'result': 'ok'})
        else:
            response = jsonify({'result': 'not ok'})
            response.status_code = 404
        return response


class NewAvatar(Resource):
    def patch(self, user_id):
        parse = reqparse.RequestParser()
        parse.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')
        args = parse.parse_args()
        image_file = args['file']
        image_file.save(f"data/image/{user_id}.jpg")
        if dbm.add_avatar(user_id, image_file):
            response = jsonify({'result': 'ok'})
        else:
            response = jsonify({'result': 'not ok'})
            response.status_code = 404
        return response


class ChangePassword(Resource):
    def patch(self, login):
        json_data = request.get_json(force=True)
        email = json_data['email']
        old_password = json_data['old_password']
        new_password = json_data['new_password']
        if dbm.change_password(login, email, old_password, new_password):
            response = jsonify({'result': 'ok'})
        else:
            response = jsonify({'result': 'not ok'})
            response.status_code = 404
        return response


class ForgotPassword(Resource):
    def patch(self, login):
        json_data = request.get_json(force=True)
        email = json_data['email']
        if dbm.forgot_password(login, email):
            response = jsonify({'result': 'ok'})
        else:
            response = jsonify({'result': 'not ok'})
            response.status_code = 404
        return response


class AddToFavouriteSpell(Resource):
    def post(self, login):
        json_data = request.get_json(force=True)
        uuid = json_data['email']
        if dbm.add_to_favourite_spell(uuid, user_id):
            response = jsonify({'result': 'ok'})
        else:
            response = jsonify({'result': 'not ok'})
            response.status_code = 404
        return response


# class NewsResource(Resource):
#     def get(self):
#         return jsonify({
#             'news':
#                 []
#             }
#         )
#     def post(self):
#         parser = reqparse.RequestParser()
#         parser.add_argument('title', required=True)
#         parser.add_argument('content', required=True)
#         parser.add_argument('user_id', required=True, type=int)
#         args = parser.parse_args()
#         return jsonify({'id': id})


db_session.global_init("db/blogs.db")
api.add_resource(UserAuth, '/user/registration')
api.add_resource(NewsResource, '/')
app.run()

#http://127.0.0.1:5000/4?title=werty&content=werty&user_id=234
