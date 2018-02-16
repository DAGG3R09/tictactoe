from flask_restful import Resource
from flask import request

from bson import ObjectId

from dao.session import get_session
from dao.user import get_user_by_id
from dao.game_instance import get_game_instance
from dao.game_instance import get_all_game_instances
from dao.game_instance import create_game_instance

from views import game_instance as gameview

from validators.session import authenticate_user
from validators.game_instance import validate_create_game_instance


class GameInstance(Resource):
    
    def get(self, game_id = None):
        params = request.args.to_dict()

        if not params:
            return {"response" : "Bad Request"}, 400

        if not authenticate_user(params.get("token")):
            return {"response" : "Unauthorized Access"}, 401
        
        if game_id:
            game = get_game_instance(game_id)

            if not game:
                return {"response" : "Game not Found"}, 404
            return {"response" : gameview.single(game)}
        
        game_instances = get_all_game_instances()

        return {"response:" : (gameview.multiple(game_instances))}

    def post(self):
        payload = request.json
        params = request.args.to_dict()

        if not payload or not params:
            return {"response:" : "Bad Request"}, 400

        if not validate_create_game_instance(payload):
            return {"response:" : "Bad Request"}, 400
            
        if not authenticate_user(params.get("token")):
            return {"response" : "Unauthorized Access"}, 401

        session = get_session(params.get("token"))
        user1_id = session['user']
        user2_id = ObjectId(str(payload['user']))

        gi = create_game_instance(user1_id, user2_id)
        
        return {"response" : str(gi)}

    def put(self):
        payload = request.json
        