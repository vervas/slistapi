from flask.ext.restful import Resource, fields, marshal_with


resource_fields = {
    'name': fields.String,
    'priority': fields.Integer
}


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

class Items(Resource):
    def get(self):
        pass

    def post(self):
        pass
