from flask.ext.restful import reqparse, abort, Resource, fields, marshal_with
from flask.ext.login import login_required
from model.item import Item
from database import MongoConnection
from bson.objectid import ObjectId
from pymongo.errors import InvalidId


parser = reqparse.RequestParser()
parser.add_argument('name', type=str)

resource_fields = {
    'name': fields.String,
    'items': fields.List(fields.Nested(Item)),
    'users': fields.List(fields.String)
}


LISTS = MongoConnection(db='slistapi', collection='lists').db


class List(Resource):

    @marshal_with(resource_fields)
    @login_required
    def get(self, list_id):
        try:
            return LISTS.find_one({"_id": ObjectId(list_id)})
        except InvalidId:
            abort(404, message="List {} doesn't exist".format(list_id))

    @login_required
    def delete(self, list_id):
        try:
            LISTS.remove({"_id": ObjectId(list_id)})
            return '', 204
        except InvalidId:
            abort(404, message="List {} doesn't exist".format(list_id))

    @login_required
    def put(self, list_id):
        pass


class Lists(Resource):
    @login_required
    def get(self):
        lists = {}
        for list_ in LISTS.find():
            lists[list_.pop("_id").__str__()] = list_

        return lists

    @login_required
    def post(self):
        args = parser.parse_args()
        list_id = LISTS.insert({'name': args['name'], 'items': [], 'users': []})
        return list_id.__str__(), 201
