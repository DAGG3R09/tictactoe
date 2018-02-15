from flask_restful import Resource
from flask import request

from dao.session import get_session
from dao.users import get_user_by_id

class GameInstance(Resource):
    
    def get(self, game_id = None):
        params = request.args.to.dict()

        session = get_session(params['token'])
        current_user = session['user']

        print ("\n Current User: ", get_user_by_id(current_user), "\n")

        