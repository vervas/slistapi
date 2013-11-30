from flask import Flask
from flask.ext.restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

ITEMS = {
    'item1': {'task': 'build an API'},
    'item2': {'task': '?????'},
    'item3': {'task': 'profit!'},
}


def abort_if_item_doesnt_exist(item_id):
    if item_id not in ITEMS:
        abort(404, message="Item {} doesn't exist".format(item_id))

parser = reqparse.RequestParser()
parser.add_argument('task', type=str)


# Item
#   show a single item item and lets you delete them
class Item(Resource):
    def get(self, item_id):
        abort_if_item_doesnt_exist(item_id)
        return ITEMS[item_id]

    def delete(self, item_id):
        abort_if_item_doesnt_exist(item_id)
        del ITEMS[item_id]
        return '', 204

    def put(self, item_id):
        args = parser.parse_args()
        task = {'task': args['task']}
        ITEMS[item_id] = task
        return task, 201


# ItemList
#   shows a list of all items, and lets you POST to add new tasks
class ItemList(Resource):
    def get(self):
        return ITEMS

    def post(self):
        args = parser.parse_args()
        item_id = 'item%d' % (len(ITEMS) + 1)
        ITEMS[item_id] = {'task': args['task']}
        return ITEMS[item_id], 201

##
## Actually setup the Api resource routing here
##
api.add_resource(ItemList, '/items')
api.add_resource(Item, '/items/<string:item_id>')


if __name__ == '__main__':
    app.run(debug=True)


