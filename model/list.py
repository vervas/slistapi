from flask.ext.restful import reqparse, abort, Resource, fields, marshal_with
from model.item import Item
from database import MongoConnection
from bson.objectid import ObjectId



def abort_if_list_doesnt_exist(list_id):
    if list_id not in LISTS:
        abort(404, message="List {} doesn't exist".format(list_id))


parser = reqparse.RequestParser()
parser.add_argument('name', type=str)


resource_fields = {
    'name': fields.String,
    'items': fields.List(fields.Nested(Item))
}


LISTS = MongoConnection(db='slistapi', collection='lists').db


class List(Resource):
    @marshal_with(resource_fields)
    def get(self, list_id):
        return LISTS.find_one({"_id": ObjectId(list_id)})

    def delete(self, list_id):
        LISTS.remove({"_id": ObjectId(list_id)})
        return '', 204


class Lists(Resource):
    def get(self):
        lists = {}
        for list_ in LISTS.find():
            lists[list_.pop("_id").__str__()] = list_
        return lists

    def post(self):
        args = parser.parse_args()
        list_id = LISTS.insert({'name': args['name'], 'items': []})
        return list_id.__str__(), 201
