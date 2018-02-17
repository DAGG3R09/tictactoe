
def single(game_instance_object):
    return {
        "game_id" : str(game_instance_object.get("_id")),
        "user1" : str(game_instance_object.get('user1')),
        "user2" : str(game_instance_object.get('user2')),
        "cstate" : game_instance_object.get('cstate'),
        "status" : game_instance_object.get('status'),
        "next player" : str(game_instance_object.get('next_player')),
        "winner" : str(game_instance_object.get('winner')),
    }

def multiple(game_instance_objects):
    
    if not game_instance_objects:
        return []

    return [
        single(game_instance_object) 
        for game_instance_object in game_instance_objects
    ]    