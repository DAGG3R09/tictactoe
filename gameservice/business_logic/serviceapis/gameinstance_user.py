
from flask_restful import Resource
from flask import request

from dao.session import get_session
from dao.game_instance import get_games_by_user
from dao.user import get_username_by_id

from views.game_instance import multiple

from validators.session import authenticate_user

from views.gameinstance_user import multiple

class GameInstanceUser(Resource):
    def get(self):

        params = request.args.to_dict()
        if not params:
            return {"response": "Bad Request"}, 400

        if not authenticate_user(params.get("token")):
            return {"response": "Unauthorized Access"}, 401

        session = get_session(params.get("token"))
        user_id = session["user"]
        game_instances = get_games_by_user(user_id)
        return {

            "response": multiple(game_instances)
        }
