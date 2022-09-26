import os
from datetime import timedelta

from flask import Flask
from flask_restful import Api

from flask_jwt_extended import JWTManager

from resources.user import *
from resources.message import *
from resources.token import *
from flask_cors import CORS

# create Flask app

app = Flask(__name__)

# adjust attributes of app
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=3)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# use database specified by DATABASE_URL environment variable. and if that's not available, use sqlite by default
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
# if the database is postgres, change url prefix to postgresql instead of postgres (postgres is changed to postgresql)
app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].replace('postgres://', 'postgresql://')
# secret key for JWT
app.secret_key = '!@#$%'

# initialize api to manage endpoints using flask_restful
api = Api(app)
# initialize JWT manager to manage JWT tokens
jwt = JWTManager(app)

# enable CORS to support cross-origin requests
CORS(app)

# add SignupResource as /signup endpoint
api.add_resource(SignupResource, '/signup/')
# add LoginResource as /login endpoint
api.add_resource(LoginResource, '/login/')
# add MessageResource as /chats endpoint
api.add_resource(MessageResource, '/chats/')
# add TokenValidation as /token_validation endpoint
api.add_resource(TokenValidation, '/token_validation/')

# run the app
if __name__ == '__main__':
    db.init_app(app)
    db.create_all(app=app)
    app.run(port=5000, debug=True)
