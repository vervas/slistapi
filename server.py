from flask import Flask
from flask.ext.restful import Api
from model import lists, items, users

app = Flask(__name__)
app.secret_key= 'XUE8bTX/BaqE/C3m5VgBAA=='

api = Api(app)


api.add_resource(lists.Lists, '/lists')
api.add_resource(lists.List, '/lists/<string:list_id>')

api.add_resource(items.Items, '/lists/<string:list_id>/items')
api.add_resource(items.Item, '/lists/<string:list_id>/items/<string:name>')

api.add_resource(users.Users, '/users')
api.add_resource(users.User, '/users/<string:user_id>')

api.add_resource(lists.ListUser, '/lists/<string:list_id>/users/<string:user_id>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
