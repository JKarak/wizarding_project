import flask
from flask import Flask, jsonify
from flask_restful import reqparse, abort, Api, Resource
from flask import request
from flask_restful import Resource
from data import db_session
from data.news import News

app = Flask(__name__)
api = Api(app)


class UserAuth(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        #parser - это prorerties
        parser.add_argument('login', required=True)
        parser.add_argument('password', required=True)
        args = parser.parse_args()
        if entrance_user(args.login, args.password):
            response = jsonify({'result': 'ok'})
        else:
            response = jsonify({'result': 'not ok'})
            response.status_code = 404
        return response


class UserRegistration(Resource):
    def post(self):
        json_data = request.get_json()


class NewsResource(Resource):
    def get(self):
        session = db_session.create_session()
        news = session.query(News).all()
        return jsonify({
            'news':
                [item.to_dict(only=('title', 'content', 'user.name'))
                 for item in news]
            }
        )
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('title', required=True)
        parser.add_argument('content', required=True)
        parser.add_argument('user_id', required=True, type=int)
        args = parser.parse_args()
        print(args)
        session = db_session.create_session()
        news = News()
        news.title = args['title']
        news.content = args['content']
        news.user_id =args['user_id']
        session.add(news)
        session.commit()
        id = session.query(News).filter(News.title == title).id
        return jsonify({'id': id})


db_session.global_init("db/blogs.db")
api.add_resource(UserAuth, '/user/registration')
api.add_resource(NewsResource, '/')
app.run()

#http://127.0.0.1:5000/4?title=werty&content=werty&user_id=234
