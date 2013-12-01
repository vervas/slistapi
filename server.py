from flask import request, Flask
from flask.ext.restful import Api
from flask.ext.login import LoginManager, login_user, logout_user, login_required
from model import lists, items, users
from itsdangerous import URLSafeTimedSerializer


app = Flask(__name__)
app.secret_key= 'XUE8bTX/BaqE/C3m5VgBAA=='

api = Api(app)

login_manager = LoginManager()
login_manager.init_app(app)

login_serializer = URLSafeTimedSerializer(app.secret_key)

@login_manager.user_loader
def load_user(user_id):
    return users.User.get(user_id)

@login_manager.token_loader
def load_token(token):
    max_age = app.config["REMEMBER_COOKIE_DURATION"].total_seconds()

    data = login_serializer.loads(token, max_age=max_age)

    #Find the User
    user = users.User.get(data[0])

    #Check Password and return user or None
    if user and data[1] == user.password:
        return user
    return None

@app.route("/login", methods=["POST"])
def login():
    user = users.User()
    login_user(user.authenticate(request.form['username'], request.form['password']))
    return "Logged in"

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return "Logged out"


api.add_resource(lists.Lists, '/lists')
api.add_resource(lists.List, '/lists/<string:list_id>')

api.add_resource(items.Items, '/lists/<string:list_id>/items')
api.add_resource(items.Item, '/lists/<string:list_id>/items/<string:name>')

api.add_resource(users.Users, '/users')
api.add_resource(users.User, '/users/<string:user_id>')

if __name__ == '__main__':
    app.config["REMEMBER_COOKIE_DURATION"] = timedelta(days=14)
    app.run(debug=True)
