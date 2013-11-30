from flask.ext.restful import reqparse, abort, Resource, fields, marshal_with
from model.item import Item
from database import MongoConnection



def abort_if_list_doesnt_exist(list_id):
    if list_id not in LISTS:
        abort(404, message="List {} doesn't exist".format(list_id))


parser = reqparse.RequestParser()
parser.add_argument('name', type=str)


resource_fields = {
    'name': fields.String,
    #'items': fields.List(fields.Nested(Item))
}



LISTS = MongoConnection(db='slistapi', collection='lists').db


class ListDao(object):
    def __init__(self, list_id, name):
        self.list_id = list_id
        self.name = name
        self.its = {}


class List(Resource):
    @marshal_with(resource_fields)
    def get(self, list_id):
        abort_if_list_doesnt_exist(list_id)
        return LISTS[list_id]

    def delete(self, list_id):
        abort_if_list_doesnt_exist(list_id)
        del LISTS[list_id]
        return '', 204


class Lists(Resource):
    def get(self):
        return LISTS

    def post(self):
        args = parser.parse_args()
        list_id = 'list%d' % (len(LISTS) + 1)
        LISTS[list_id] = {'name': args['name']}
        return LISTS[list_id], 201
