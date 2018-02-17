from jsonschema import validate
from dao.game_instance import get_game_instance

schema =  {
    "type" : "object",
    "properties" : {
        "user" : {"type" : "string"}
    }
}

def validate_create_game_instance(payload):
    try:
        validate(payload, schema)
        return True
    except:
        print ("create game failed.")
        return False

def check_acceptance(user_id, game_obj_id):
    game_obj = get_game_instance(game_obj_id)

    print(type(game_obj))

    return False
