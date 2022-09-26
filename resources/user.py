# this file contains the UserModel class (which is an ORM for users table in the database) and resources for login
# and signup endpoints

from flask import request
from flask_jwt_extended import create_access_token

from db import db
from flask_restful import Resource
import hmac


class UserModel(db.Model):
    # uses 'users' as table name
    __tablename__ = 'users'
    # defining columns
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)

    @classmethod
    def find_by_username(cls, name):
        '''
        :param name: username
        :return: UserModel object if found, None otherwise
        '''
        name = name.lower()
        return cls.query.filter_by(username=name).first()

    @classmethod
    def find_by_id(cls, _id):
        '''
        :param _id: id of the user
        :return: UserModel object if found, None otherwise
        '''
        return cls.query.filter_by(id=_id).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def json(self):
        return {
            'id': self.id,
            'username': self.username
        }


# resource for signup endpoint
class SignupResource(Resource):
    # method handling POST requests
    def post(self):
        # fetch the json data from the request
        data = request.get_json()
        # check if the username is already taken
        if UserModel.find_by_username(data['username']):
            # if it is, return a message and 400 status code. note: return value will be automatically converted to json
            # by flask_restful
            return {'message': 'User with same username already exists'.format()}, 400
        # else, create a new user
        user = UserModel(data['username'], data['password'])
        # save the user to the database
        user.save()
        # return a message and 201 status code indicating that the user was created
        return {'message': 'User created successfully.'}, 201


# resource for login endpoint
class LoginResource(Resource):
    def post(self):
        data = request.get_json()
        user = UserModel.find_by_username(data['username'])
        # if user is found, compare the password
        if user and hmac.compare_digest(user.password, data['password']):
            # if password matches, create a jwt access token based on user id and return it
            access_token = create_access_token(identity=user.id, fresh=True)
            return {'access_token': access_token, 'user_id': user.id}, 200
        # else, return a message and 401 status code
        return {'message': 'Invalid credentials.'}, 401
