from flask.ext.restful import Resource, fields, marshal_with

resource_fields = {
        'name': fields.String,
        'priority': fields.Integer,
        }

class ItemDao(object):
    def __init__(self, item_id, name, priority):
        self.item_id= item_id
        self.name = name
        self.priority = priority

class Item(Resource):
    @marshal_with(resource_fields)
    def get(self, **kwargs):
        pass

    def delete(self, **kwargs):
        pass

    def post(self, **kwargs):
        pass

    def put(self, **kwargs):
        pass
