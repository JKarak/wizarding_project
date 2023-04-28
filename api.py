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
        json_data = request.json
        login = json_data['login']
        key = json_data['key']
        email = json_data['email']
        name = json_data['name']
        print(login, key, email, name)
        if dbm.add_user(login, key, email, name):
            response = jsonify({'result': 'ok'})
        else:
            response = jsonify({'result': 'not ok'})
            response.status_code = 404
        return response


class UserInfo(Resource):
    def get(self, email):
        if dbm.get_user_info(email):
            response = dbm.get_user_info(email)
        else:
            response = jsonify({'result': 'not ok'})
            response.status_code = 404
        return response


class NewAvatar(Resource):
    def patch(self, email):
        parse = reqparse.RequestParser()
        parse.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')
        args = parse.parse_args()
        image_file = args['file']
        image_file.save(f"data/image/{email}.jpg")
        if dbm.add_avatar(email, image_file):
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


class FavouriteSpells(Resource):
    def get(self, user_id):
        if dbm.spells_favourite(user_id):
            response = dbm.spells_favourite(user_id)
        else:
            response = jsonify({'result': 'not ok'})
            response.status_code = 404
        return response
    def post(self, user_id):
        json_data = request.get_json(force=True)
        uuid = json_data['uuid']
        if dbm.add_to_favourite_spell(uuid, user_id):
            response = jsonify({'result': 'ok'})
        else:
            response = jsonify({'result': 'not ok'})
            response.status_code = 404
        return response


class FavouritePotions(Resource):
    def get(self, user_id):
        if dbm.potions_favourite(user_id):
            response = dbm.potions_favourite(user_id)
        else:
            response = jsonify({'result': 'not ok'})
            response.status_code = 404
        return response
    def post(self, user_id):
        json_data = request.get_json(force=True)
        uuid = json_data['uuid']
        if dbm.add_to_favourite_spell(uuid, user_id):
            response = jsonify({'result': 'ok'})
        else:
            response = jsonify({'result': 'not ok'})
            response.status_code = 404
        return response


class FavouriteAll(Resource):
    def get(self, user_id):
        if dbm.all_favourite(user_id):
            response = dbm.all_favourite(user_id)
        else:
            response = jsonify({'result': 'not ok'})
            response.status_code = 404
        return response


class ViewedPotions(Resource):
    def get(self, user_id):
        if dbm.potions_favourite(user_id):
            response = dbm.potions_favourite(user_id)
        else:
            response = jsonify({'result': 'not ok'})
            response.status_code = 404
        return response
    def post(self, user_id):
        json_data = request.get_json(force=True)
        uuid = json_data['uuid']
        if dbm.add_to_viewed_potions(uuid, user_id):
            response = jsonify({'result': 'ok'})
        else:
            response = jsonify({'result': 'not ok'})
            response.status_code = 404
        return response


class ViewedSpells(Resource):
    def post(self, user_id):
        json_data = request.get_json(force=True)
        uuid = json_data['uuid']
        if dbm.add_to_viewed_spells(uuid, user_id):
            response = jsonify({'result': 'ok'})
        else:
            response = jsonify({'result': 'not ok'})
            response.status_code = 404
        return response


class Potion(Resource):
    def get(self, id):
        if dbm.get_potion(id):
            response = dbm.get_potion(id)
        else:
            response = jsonify({'result': 'not ok'})
            response.status_code = 404
        return response

class Spell(Resource):
    def get(self, id):
        if dbm.get_spell(id):
            response = dbm.get_spell(id)
        else:
            response = jsonify({'result': 'not ok'})
            response.status_code = 404
        return response

class SpellByType(Resource):
    def get(self, type):
        if dbm.get_spell_by_type(type):
            response = dbm.get_spell_by_type(type)
        else:
            response = jsonify({'result': 'not ok'})
            response.status_code = 404
        return response

# class PotionsList(Resource):
#     def get(self, id):
#         if dbm.get_potion(id):
#             response = dbm.get_potion(id)
#         else:
#             response = jsonify({'result': 'not ok'})
#             response.status_code = 404
#         return response


db_session.global_init("db/blogs.db")
api.add_resource(UserAuth, '/user/auth')
api.add_resource(UserRegistration, '/user/registration')
api.add_resource(UserInfo, '/user/<string:email>/info')
api.add_resource(NewAvatar, '/user/<string:email>/changeavatar')
api.add_resource(ForgotPassword, '/user/<string:login>/forgotpassword')
api.add_resource(FavouriteSpells, '/user/<string:user_id>/favourite/spells')
api.add_resource(FavouritePotions, '/user/<string:user_id>/favourite/potions')
api.add_resource(FavouriteAll, '/user/<string:user_id>/favourite/all_favourite')
api.add_resource(ViewedPotions, '/viewed/<string:user_id>/potions')
api.add_resource(ViewedSpells, '/viewed/<string:user_id>/spells')
api.add_resource(Potion, '/potions/<string:id>')
api.add_resource(Spell, '/spells/<string:id>')
api.add_resource(SpellByType, '/spells/<string:type>')
app.run()

#http://127.0.0.1:5000/4?title=werty&content=werty&user_id=234
