from flask.ext.restful import reqparse, abort, Resource, fields, marshal_with
from model.items import Item
from database import MongoConnection
from bson.objectid import ObjectId
from pymongo.errors import InvalidId


parser = reqparse.RequestParser()
parser.add_argument('name', type=str)
parser.add_argument('user_id', type=str)

resource_fields = {
    'name': fields.String,
    'items': fields.List(Item),
    'users': fields.List(fields.String)
}


LISTS = MongoConnection(db='slistapi', collection='lists').db


class List(Resource):

    @marshal_with(resource_fields)
    def get(self, list_id):
        try:
            return LISTS.find_one({"_id": ObjectId(list_id)})
        except InvalidId:
            abort(404, message="List {} doesn't exist".format(list_id))

    def delete(self, list_id):
        try:
            LISTS.remove({"_id": ObjectId(list_id)})
            return '', 204
        except InvalidId:
            abort(404, message="List {} doesn't exist".format(list_id))

    def put(self, list_id):
        args = parser.parse_args()
        try:
            item = LISTS.update({'_id': ObjectId(list_id)},
                    {'$push':
                        {
                            'users': args['user_id']
                        }
                    },
                    upsert=False)
            return item['updatedExisting'], 201
        except InvalidId:
            abort(404, message="List {} doesn't exist".format(list_id))


class ListUser(Resource):
    def delete(self, list_id, user_id):
        try:
            item = LISTS.update({'_id': ObjectId(list_id)},
                    {'$pop':
                        {
                            'users': user_id
                        }
                    },
                    upsert=False)
            return item['updatedExisting'], 201
        except InvalidId:
            abort(404, message="List {} doesn't exist".format(list_id))

class Lists(Resource):
    def get(self):
        lists = {}
        for list_ in LISTS.find():
            lists[list_.pop("_id").__str__()] = list_

        return lists

    def post(self):
        args = parser.parse_args()
        list_id = LISTS.insert({'name': args['name'], 'items': [], 'users': [args['user_id']]})
        return list_id.__str__(), 201
