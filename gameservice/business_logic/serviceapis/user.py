from flask_restful import Resource
from flask import request
from validators.user import validate_user
from validators.session import authenticate_user

from views import user as userview
from dao.user import get_user_by_id, get_all_user, get_user_by_mail, create_user
from dao.session import get_session

class User(Resource):

    def get(self, user_id = None):
        
        params = request.args.to_dict()      

        if not params:
            return {"response" : "Bad Request"}, 400
            
        if not authenticate_user(params.get('token')):
            return {"response" : "Unauthorised Access"}, 401

        if user_id:
            user = get_user_by_id(user_id)

            if not user:
                return {"response" : "User not found"}, 404
            return {"response" : userview.single(user) }

        users = get_all_user()
        return {"response" : userview.multiple(users) }


    def post(self):
        payload = request.json
        if not validate_user(payload):
            return {"response" : "Bad request"}, 401

        email = payload['email']
        user = get_user_by_mail(email)
        if user:
            return {"response" : "Email already used"}, 401

        create_user(payload)
        user = get_user_by_mail(email)
        return userview.single(user)
