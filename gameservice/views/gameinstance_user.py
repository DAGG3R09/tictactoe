from dao.user import get_username_by_id


def single(game_instance):
    # print (game_instance)

    game_id = str(game_instance['_id'])
    challenger = get_username_by_id(game_instance['user1'])
    opponent = get_username_by_id(game_instance['user2'])
    next_player = get_username_by_id(game_instance['next_player'])
    status = game_instance['status']

    return {
        "game_id": game_id,
        "challenger": challenger,
        "opponent": opponent,
        "next_player": next_player,
        "status": status
    }


def multiple(game_instances):
    return [single(game_instance) for game_instance in game_instances]