from flask_restful import Resource,reqparse
from flask_jwt import jwt_required, current_identity
from flask import jsonify
from models.game import GameModel
from models.user import UserModel

class Game(Resource):
    @jwt_required()
    def get(self):
        user=current_identity
        ingame=GameModel.check_if_in_game(user.username)
        if ingame:
            return{"message": "Username already in game","game_id":ingame.id}
        foundUser=GameModel(user.username)
        return foundUser.create_game(user.username)
    @jwt_required()
    def delete(self):
        info= GameModel.check_if_in_game(current_identity.username)
        if(info):
            GameModel.leave_game(current_identity.username)
            return {'message':"You have left the game"}

class PlayerMove(Resource):
    parser=reqparse.RequestParser()
    parser.add_argument('move',
                         type=int,
                         required=True,
                         help="Must select a move")
    parser.add_argument('symbol',
                         type=str,
                         required=True,
                         help="Must use symbol")
    @jwt_required()
    def put(self):
        data=PlayerMove.parser.parse_args()
        ingame=GameModel.check_if_in_game(current_identity.username)
        if ingame:
            if ingame.make_move(data['move'],data['symbol']):
                return {"message":"Move has been made"}
            return {"message":"Not Player Turn/Space already used"}
        return{"message":"User not in game"}
class CPUMove(Resource):
    @jwt_required()
    def put(self):
        ingame=GameModel.check_if_in_game(current_identity.username)
        if ingame:
            if ingame.cpu_move():
                return {"message":"Move has been made"}
            return {"message":"Not CPU Turn"}
        return{"message":"User not in game"}
class CheckStatus(Resource):
    @jwt_required()
    def get(self):
        ingame=GameModel.check_if_in_game(current_identity.username)
        if ingame:
            status=ingame.check_game_status()
            user=UserModel.find_by_username(current_identity.username)
            if status["winner"]=="none":
                return{"Game Status":"Still going"}
            elif status["winner"]=="player1":
                user.save_win()
                return{"Game Status":"Game Won"}
            elif status["winner"]=="tie":
                user.save_tie()
                return{"Game Status":"Tie"}
            else:
                user.save_lose()
                return{"Game Status":"Game Lost"}



