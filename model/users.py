from flask.ext.restful import reqparse, abort, Resource, fields, marshal_with
from database import MongoConnection
from bson.objectid import ObjectId
from pymongo.errors import InvalidId


parser = reqparse.RequestParser()
parser.add_argument('name', type=str)
parser.add_argument('password', type=str)

resource_fields = {
        'name': fields.String,
        'password': fields.String
    }


USERS = MongoConnection(db='slistapi', collection='users').db


class User(Resource):
    def delete(self):
        try:
            USERS.remove({"_id": ObjectId("string")})
            return '', 204
        except InvalidId:
            abort(404, message="List {} doesn't exist".format("string"))


class Users(Resource):
    def get(self):
        users = {}
        for user in USERS.find():
            users[user.pop("_id").__str__()] = user

        return users

    def post(self):
        args = parser.parse_args()
        list_id = USERS.insert({'name': args['name'], 'password': args['password']})
        return list_id.__str__(), 201

