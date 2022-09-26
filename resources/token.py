# models a simple resource that can be used to check if an access token is expired or not
from flask_restful import Resource
from flask_jwt import jwt_required


class TokenValidation(Resource):
    #by simply adding the jwt_required decorator, we can check if the access token is valid or not
    @jwt_required()
    def post(self):
        #if the token is valid, return a message and 200 status code
        return {'message': 'valid JWT token'}, 200