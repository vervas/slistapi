from flask.ext.restful import reqparse, abort, Resource, fields, marshal_with
from flask.ext.bcrypt import generate_password_hash
from model.lists import LISTS
from database import MongoConnection
from bson.objectid import ObjectId
from pymongo.errors import InvalidId


parser = reqparse.RequestParser()
parser.add_argument('username', type=str)
parser.add_argument('password', type=str)

resource_fields = {
    'username': fields.String,
    'password': fields.String
}


USERS = MongoConnection(collection='users').db


class User(Resource):
    def __init__(self, user_id=None, username=None, password=None):
        self.id = user_id
        self.username = username
        self.password = password

    @marshal_with(resource_fields)
    def get(self, user_id):
        try:
            return USERS.find_one({"_id": ObjectId(user_id)})
        except InvalidId:
            abort(404, message="User {} doesn't exist".format(user_id))

    def delete(self, user_id):
        try:
            LISTS.update({'users': user_id},
                         {'$pop':
                             {
                                 'users': user_id
                             }
                         },
                         upsert=False, multi=True)
            USERS.remove({"_id": ObjectId(user_id)})
            return '', 204
        except InvalidId:
            abort(404, message="User {} doesn't exist".format(user_id))


class Users(Resource):
    def get(self):
        users = {}
        for user in USERS.find():
            users[user.pop("_id").__str__()] = user

        return users

    def post(self):
        args = parser.parse_args()
        list_id = USERS.insert({'username': args['username'], 'password': generate_password_hash(args['password'])})
        return list_id.__str__(), 201
