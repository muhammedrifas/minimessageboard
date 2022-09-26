# this file contains the MessageModel class (which is an ORM for messages table in the database) and resource for
# chats endpoint

from flask import request
from flask_jwt_extended import jwt_required

from db import db
from flask_restful import Resource
import datetime
from resources.user import UserModel


class MessageModel(db.Model):
    # uses 'messages' as table name
    __tablename__ = 'messages'
    # defining columns
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=True)
    message = db.Column(db.String(80), nullable=False)
    date = db.Column(db.String(80), nullable=False)
    # uses user id which is a foreign key to find all messages by a user
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # specify relationship between users and messages tables
    user = db.relationship('UserModel')

    def save(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        return {
            'id': self.id,
            'title': self.title,
            'message': self.message,
            'date': self.date,
            'user_id': self.user_id,
            'username': UserModel.find_by_id(self.user_id).username
        }

    def __init__(self, title, message, date, user_id):
        self.title = title
        self.message = message
        self.date = date
        self.user_id = user_id


# resource for chats endpoint
class MessageResource(Resource):
    @jwt_required()
    def get(self):
        limit = 50
        # fetch first 'limit' number of messages from db after sorting by date descending
        messages = MessageModel.query.order_by(MessageModel.date.desc()).limit(limit).all()
        return {'messages': [message.json() for message in messages]}, 200

    @jwt_required()
    def post(self):
        data = request.get_json()
        # check if user_id in the request is valid
        if not UserModel.find_by_id(data['user_id']):
            return {'message': 'Invalid user!'}, 400
        # get current date and format it in yyyy-mm-dd hh:mm am/pm format
        date = datetime.datetime.now().strftime("%Y-%m-%d %I:%M %p")
        # create a new message object
        message = MessageModel(data['title'], data['message'], date, data['user_id'])
        # save the message to the database
        message.save()
        return {'message': 'Message created successfully.'}, 201

    @jwt_required()
    def delete(self):
        # fetch the json data from the request
        data = request.get_json()
        # check if the message exists and user is the owner of the message
        message = MessageModel.query.filter_by(id=data['id'], user_id=data['user_id']).first()
        # if found, delete the message from the database
        if message:
            db.session.delete(message)
            db.session.commit()
            return {'message': 'Message deleted successfully.'}, 200
        return {'message': 'Message not found.'}, 404
