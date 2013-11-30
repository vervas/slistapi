from flask import Flask
from flask.ext.restful import Api
from model import lists, items

app = Flask(__name__)
api = Api(app)

api.add_resource(lists.Lists, '/lists')
api.add_resource(lists.List, '/lists/<string:list_id>')

api.add_resource(items.Items, '/lists/<string:list_id>/items')
api.add_resource(items.Item, '/lists/<string:list_id>/items/<string:name>')

if __name__ == '__main__':
    app.run(debug=True)
