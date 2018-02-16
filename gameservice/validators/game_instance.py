from jsonschema import validate

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