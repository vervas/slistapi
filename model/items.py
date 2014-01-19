from flask.ext.restful import reqparse, abort, Resource, fields
from database import MongoConnection
from bson.objectid import ObjectId
from pymongo.errors import InvalidId


parser = reqparse.RequestParser()
parser.add_argument('name', type=str)
parser.add_argument('priority', type=int)

LISTS = MongoConnection(collection='lists').db


class Item(Resource, fields.Raw):
    def delete(self, list_id, name):
        try:
            LISTS.update({'_id': ObjectId(list_id)},
                         {'$pull':
                             {
                                 'items': {
                                     'name': name
                                 }
                             }
                         },
                         upsert=False)
            return '', 204
        except InvalidId:
            abort(404, message="List {} doesn't exist".format(list_id))


class Items(Resource):
    def get(self, list_id):
        try:
            return LISTS.find_one({"_id": ObjectId(list_id)})['items']
        except InvalidId:
            abort(404, message="List {} doesn't exist".format(list_id))

    def post(self, list_id):
        args = parser.parse_args()
        try:
            item = LISTS.update({'_id': ObjectId(list_id)},
                                {'$push':
                                    {
                                        'items': {
                                            '$each': [
                                                {'name': args['name'], 'priority': args['priority']}
                                            ],
                                            '$sort': {'priority': 1},
                                            '$slice': -120
                                        }
                                    }
                                },
                                upsert=False)
            return item['updatedExisting'], 201
        except InvalidId:
            abort(404, message="List {} doesn't exist".format(list_id))
