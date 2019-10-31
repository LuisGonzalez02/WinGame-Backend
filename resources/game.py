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
        if ingame["position"]!=None:
            board=ingame["info"].gameBoard()
            return{"message": "Username already in game","game_id":ingame["info"].id,"board":board,"active":ingame["info"].gameopen}
        foundUser=GameModel(user.username,False,"CPU")
        return foundUser.create_game(user.username,False)
    @jwt_required()
    def delete(self):
        info= GameModel.check_if_in_game(current_identity.username)
        if(info["position"]!=None):
            GameModel.leave_game(current_identity.username)
            return {'message':"You have left the game"}
class PVPCheckIfMove(Resource):
    @jwt_required()
    def get(self):
        user=current_identity
        ingame=GameModel.check_if_in_game(user.username)
        if ingame["position"] !=None:
            return ingame["info"].check_turn(ingame["position"])
        return {"message":"Not in Game"}

class PVPGame(Resource):
    @jwt_required()
    def get(self):
        user=current_identity
        ingame=GameModel.check_if_in_game(user.username)
        if ingame["position"]!=None:
            board=ingame["info"].gameBoard()
            return{"message": "Username already in game","game_id":ingame["info"].id,"board":board,"active":ingame["info"].gameopen}
        foundUser=GameModel(user.username,True,"")
        return foundUser.find_game(user.username)

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
        user=UserModel.find_by_username(current_identity.username)
        if ingame["position"]!=None:
            board=ingame["info"].gameBoard()
            if ingame["info"].make_move(data['move'],data['symbol'],ingame['position']):
                status=ingame["info"].check_game_status()
                if status["winner"]=="none":
                    if ingame["info"].pvp== False:               
                        if ingame["info"].cpu_move():
                            board=ingame["info"].gameBoard()
                            status=ingame["info"].check_game_status()
                            if status["winner"]=="none":
                                return{"Game Status":"Still going","message":"Move has been made","board":board}
                            if status["winner"]=="player1":
                                user.save_win()
                                return{"Game Status":"Game Won","message":"Move has been made","board":board}
                            elif status["winner"]=="tie":
                                user.save_tie()
                                return{"Game Status":"Tie","message":"Move has been made","board":board}
                            else:
                                user.save_lose()
                                return{"Game Status":"Game Lost","message":"Move has been made","board":board}
                        return {"Game Status":"Still going","message":"Not CPU Turn","board":board}
                else:
                    board=ingame["info"].gameBoard()
                    if status["winner"]=="player1":
                        user.save_win()
                        return{"Game Status":"Game Won","message":"Move has been made","board":board}
                    elif status["winner"]=="tie":
                        user.save_tie()
                        return{"Game Status":"Tie","message":"Move has been made","board":board}
                    else:
                        user.save_lose()
                        return{"Game Status":"Game Lost","message":"Move has been made","board":board}
            return {"message":"Not Player Turn/Space already used","Game Status":"Still going","board":board}
        return{"message":"User not in game","Game Status":"Still going","board":["","","","","","","","",""]}
class CPUMove(Resource):
    @jwt_required()
    def put(self):
        ingame=GameModel.check_if_in_game(current_identity.username)
        if info["position"]!=None:
            if ingame["info"].cpu_move():
                return {"message":"Move has been made"}
            return {"message":"Not CPU Turn"}
        return{"message":"User not in game"}
class CheckStatus(Resource):
    @jwt_required()
    def get(self):
        ingame=GameModel.check_if_in_game(current_identity.username)
        if ingame["position"]!=None:
            status=ingame["info"].check_game_status()
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



