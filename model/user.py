from flask.ext.restful import Resource, fields, marshal_with
from model.list import List

resource_fields = {
        'name': fields.String,
        'lists': List,
        }

class UserDao(object):
    def __init__(self, user_id, name):
        self.user_id = user_id 
        self.name = name

class User(Resource):
    @marshal_with(resource_fields)
    def get(self, **kwargs):
        pass

    def delete(self, **kwargs):
        pass

    def post(self, **kwargs):
        pass

    def put(self, **kwargs):
