from flask import Flask
from flask_restful import Api

from business_logic.serviceapis.ping import Ping
from business_logic.serviceapis.gameinstance import GameInstance
from business_logic.serviceapis.gameinstance_user import GameInstanceUser
from business_logic.serviceapis.user import User
from business_logic.serviceapis.validation import UserValidation
from flask_cors import CORS

# from flask import request


app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
api = Api(app)


api.add_resource(Ping, '/gameservice/ping')
api.add_resource(User, '/gameservice/users', '/gameservice/users/<string:user_id>')
api.add_resource(UserValidation, '/gameservice/uservalidation')
api.add_resource(GameInstance, '/gameservice/gameinstance', '/gameservice/gameinstance/<string:game_id>')
api.add_resource(GameInstanceUser, "/gameservice/gameinstance/games")


#api.add_resource(GameInstance, '')
#api.add_resource(Move,)

if __name__=='__main__':
    app.run(debug=True, port=6756)