from jsonschema import validate
from dao.game_instance import get_game_instance

schema =  {
    "type": "object",
    "properties": {
        "user": {"type": "string"}
    }
}


def validate_create_game_instance(payload):
    """Validates the payload schema and expected schema"""

    try:
        validate(payload, schema)
        return True
    except:
        print ("create game failed.")
        return False


def check_acceptance(user_id, game_obj_id):
    """Returns True if user2 of game is accepting the game"""

    game_obj = get_game_instance(game_obj_id)

    if str(user_id) == str(game_obj.get("user2")):
        return True
    return False


def validate_new_state(current_state, new_state, position):
    """
        Returns true if there is exactly 1 change in new state
        and
        if no symbol is overwritten.
    """
    if (current_state[position[0]][position[1]] == "X"
            or
            current_state[position[0]][position[1]] == "O"):
        return False

    cnt = 1
    for i in range(0, 3):
        for j in range(0, 3):
            if current_state[i][j] != new_state[i][j]:
                cnt -= 1

    if cnt == 0:
        return True
    else:
        return False
