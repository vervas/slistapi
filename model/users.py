from flask.ext.restful import reqparse, abort, Resource, fields, Api
from flask.ext.bcrypt import generate_password_hash, check_password_hash
from flask.ext.login import login_required, UserMixin
from itsdangerous import URLSafeTimedSerializer
from database import MongoConnection
from bson.objectid import ObjectId
from pymongo.errors import InvalidId


parser = reqparse.RequestParser()
parser.add_argument('username', type=str)
parser.add_argument('password', type=str)

login_serializer = URLSafeTimedSerializer('XUE8bTX/BaqE/C3m5VgBAA==')

resource_fields = {
        'name': fields.String,
        'password': fields.String
    }


USERS = MongoConnection(db='slistapi', collection='users').db


class User(Resource, UserMixin):
    def __init__(self, user_id=None, username=None, password=None):
        self.id = user_id
        self.username = username
        self.password = password

    def authenticate(self, username, password):
        try:
            user = USERS.find_one({"username": username})
            if check_password_hash(user['password'], password):
                self.id = ObjectId(user['_id'])
                self.username = user['username']
                return self
            else:
                abort(401, message="Wrong unsername or password")
        except InvalidId:
            abort(401, message="Wrong unsername or password")
            #abort(401, message="User {} doesn't exist".format(user_id))

    def get_auth_token(self):
        """
        Encode a secure token for cookie
        """
        data = [str(self.id), self.password]
        return login_serializer.dumps(data)

    def get(self, user_id):
        try:
            user = USERS.find_one({"_id": ObjectId(user_id)})
            return User(unicode(user['_id']), user['username'])
        except InvalidId:
            abort(404, message="User {} doesn't exist".format(user_id))

    @login_required
    def delete(self, user_id):
        try:
            USERS.remove({"_id": ObjectId(user_id)})
            return '', 204
        except InvalidId:
            abort(404, message="User {} doesn't exist".format(user_id))

class Users(Resource):
    @login_required
    def get(self):
        users = {}
        for user in USERS.find():
            users[user.pop("_id").__str__()] = user

        return users

    def post(self):
        args = parser.parse_args()
        list_id = USERS.insert({'username': args['username'], 'password': generate_password_hash(args['password'])})
        return list_id.__str__(), 201

