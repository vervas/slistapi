from flask.ext.restful import reqparse, abort, Resource, fields, marshal_with
from model.lists import LISTS
from bson.objectid import ObjectId
from pymongo.errors import InvalidId


parser = reqparse.RequestParser()
parser.add_argument('name', type=str)
parser.add_argument('priority', type=int)

resource_fields = {
    'name': fields.String,
    'priority': fields.Integer
}


class Item(Resource):
    def delete(self, list_id, name):
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


class Items(Resource):
    def get(self, list_id):
        return LISTS.find_one({"_id": ObjectId(list_id)})['items']

    def post(self, list_id):
        args = parser.parse_args()
        item = LISTS.update({'_id': ObjectId(list_id)},
                {'$push':
                    {
                        'items': {
                            'name': args['name'],
                            'priority': args['priority']
                        }
                    }
                },
                upsert=False)
        return item['updatedExisting'], 201
