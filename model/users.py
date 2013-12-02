from flask.ext.restful import reqparse, abort, Resource, fields
from flask.ext.bcrypt import generate_password_hash, check_password_hash
from database import MongoConnection
from bson.objectid import ObjectId
from pymongo.errors import InvalidId


parser = reqparse.RequestParser()
parser.add_argument('username', type=str)
parser.add_argument('password', type=str)

resource_fields = {
        'name': fields.String,
        'password': fields.String
    }


USERS = MongoConnection(db='slistapi', collection='users').db


class User(Resource):
    def __init__(self, user_id=None, username=None, password=None):
        self.id = user_id
        self.username = username
        self.password = password

    def get(self, user_id):
        try:
            user = USERS.find_one({"_id": ObjectId(user_id)})
            return User(unicode(user['_id']), user['username'])
        except InvalidId:
            abort(404, message="User {} doesn't exist".format(user_id))

    def delete(self, user_id):
        try:
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

