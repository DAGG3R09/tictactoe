from pymongo import MongoClient
from bson import ObjectId
from utils import constants as gconst

client = MongoClient()
db = client.game_engine

ginstancecltn = db.game_instance

def create_game_instance(user1_obj_id, user2_obj_id):
    instance_object = {
        "user1" : user1_obj_id,
        "user2" : user2_obj_id,
        "cstate" : gconst.default_state,
        "status" : gconst.default_start_status,
        "next_player" : user1_obj_id,
        "winner": None
    }
    gi = ginstancecltn.insert_one(instance_object)
    return gi.inserted_id


def get_game_instance(game_obj_id):
    return ginstancecltn.find_one({"_id" : game_obj_id})


def get_all_game_instances():
    return ginstancecltn.find({})


def accepted_game_instance(game_obj_id):
    ginstancecltn.update_one(
        {"_id": game_obj_id},
        {"$set": {"status": gconst.accepted_status}})


def completed_game_instance(game_obj_id, winner):
    print("In completed game instance")
    ginstancecltn.update_one(
        {"_id": game_obj_id},
        {"$set": {"status": gconst.final_status, "winner": winner}})


def reset_game(game_obj_id):
    ginstancecltn.update_one(
        {"_id": game_obj_id},
        {"$set": {"cstate": gconst.default_state, "status": gconst.accepted_status, "winner": None}})


def game_draw(game_obj_id):
    ginstancecltn.update_one(
        {"_id": game_obj_id},
        {"$set": {"status": gconst.draw_status}})


def make_move(game_obj_id, new_state, next_player):
    ginstancecltn.update_one(
        {"_id" : game_obj_id},
        {"$set":
            {
                "cstate": new_state,
                "next_player": next_player

            }
        }
    )


def get_games_by_user(user_id):
    user_obj_id = ObjectId(user_id)
    return ginstancecltn.find({"$or": [{"user1": user_obj_id}, {"user2": user_obj_id}]})


if __name__ == "__main__":
    reset_game(ObjectId("5a9cfc741b2a6104c061b24f"))




