from flask_restful import Resource
from flask import request

from copy import deepcopy

from bson import ObjectId

from dao.session import get_session
from dao.user import get_user_by_id
from dao.game_instance import get_game_instance
from dao.game_instance import get_all_game_instances, make_move, completed_game_instance
from dao.game_instance import create_game_instance, accepted_game_instance

from views import game_instance as gameview

from validators.session import authenticate_user
from validators.game_instance import validate_create_game_instance
from validators.game_instance import check_acceptance, validate_new_state

from utils.game_instance import check_winning_state


class GameInstance(Resource):
    def get(self, game_id=None):
        params = request.args.to_dict()

        if not params:
            return {"response": "Bad Request"}, 400

        if not authenticate_user(params.get("token")):
            return {"response": "Unauthorized Access"}, 401

        if game_id:
            game = get_game_instance(ObjectId(game_id))

            if not game:
                return {"response": "Game not Found"}, 404
            return {"response": gameview.single(game)}
        
        game_instances = get_all_game_instances()

        return {"response:": (gameview.multiple(game_instances))}


    def post(self):
        payload = request.json
        params = request.args.to_dict()

        if not payload or not params:
            return {"response:": "Bad Request"}, 400

        if not validate_create_game_instance(payload):
            return {"response:": "Bad Request"}, 400
            
        if not authenticate_user(params.get("token")):
            return {"response": "Unauthorized Access"}, 401

        session = get_session(params.get("token"))
        user1_id = session['user']
        user2_id = ObjectId(str(payload['user']))

        gi = create_game_instance(user1_id, user2_id)
        
        return {"response": str(gi)}


    def put(self):
        payload = request.json
        params = request.args.to_dict()

        if not payload or not params:
            return {"response:": "Bad Request"}, 400

        if not authenticate_user(params.get("token")):
            return {"response": "Unauthorized Access"}, 401

        session = get_session(params.get("token"))
        user_id = session['user']
        game_obj_id = ObjectId(payload['game_id'])

        if not check_acceptance(user_id, game_obj_id):
            return {"response": "Unauthorized Access"}, 401
        
        game_obj = get_game_instance(game_obj_id)
        accepted_game_instance(game_obj_id)

        return {"response": gameview.single(game_obj)}


    def patch(self):
        """
            Make a move.
            Params : tokens
            payload: game_id, row, col
        """
        payload = request.json
        params = request.args.to_dict()

        if not payload or not params:
            return {"response:": "Bad Request"}, 400

        if not authenticate_user(params.get("token")):
            return {"response": "Unauthorized Access"}, 401

        print(payload)

        game_id = payload['game_id']
        game = get_game_instance(ObjectId(game_id))
        next_player = game['next_player']

        session = get_session(params.get("token"))
        user = session['user']

        if next_player != user:
            return {"response": "Forbidden"}, 403

        row = int(payload['row'])
        col = int(payload['col'])

        if not (0 <= row <= 2 and 0 <= col <= 2):
            return {"response:": "Bad Request"}, 400

        if user == game['user1']:
            symbol = "X"
            next_player = game['user2']
        else:
            symbol = "O"
            next_player = game['user1']

        new_state = deepcopy(game["cstate"])
        new_state[row][col] = symbol
        # print("neww", new_state)

        if not validate_new_state(game["cstate"], new_state, (row, col)):
            return {"response:": "Bad Request"}, 400

        new_status = game['status']

        if check_winning_state(new_state, row, col):
            print("Win state:", row, " ", col)
            winner = user
            completed_game_instance(ObjectId(game_id), winner)

        make_move(ObjectId(game_id), new_state, next_player)

        game = get_game_instance(ObjectId(game_id))
        # return {"response": new_state}

        return {"response": gameview.single(game)}, 200