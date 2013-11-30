from flask import Flask
from flask.ext.restful import Api
from model import list

app = Flask(__name__)
api = Api(app)

api.add_resource(list.Lists, '/lists')
api.add_resource(list.List, '/lists/<string:list_id>')

if __name__ == '__main__':
    app.run(debug=True)
