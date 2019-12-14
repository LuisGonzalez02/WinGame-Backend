from flask_restful import Resource,reqparse
from flask_jwt import jwt_required, current_identity
from flask import jsonify
from models.game import GameModel
from models.user import UserModel

class Game(Resource):
    @jwt_required()
    def get(self):
        ingame=GameModel.check_if_in_game(current_identity.username)
        if ingame==None:
            ingame=GameModel(current_identity.username,"solo","CPU")
        return{"board":ingame.boardTiles,"active":ingame.gameopen,"player1":ingame.player1,"player2":ingame.player2,"status":ingame.gameStatus}
    @jwt_required()
    def delete(self):
        info= GameModel.check_if_in_game(current_identity.username)
        if info!=None:
            GameModel.leave_game(current_identity.username)
            return {'message':"You have left the game"}
        return {"message":"Not in game"}
class PVPCheckIfMove(Resource):
    @jwt_required()
    def get(self):
        ingame=GameModel.check_if_in_game(current_identity.username)
        user=UserModel.find_by_username(current_identity.username)
        if ingame !=None:
            return {"message": "User in Game","status":ingame.gameStatus,"active":ingame.gameopen, "board":ingame.boardTiles,"record":user.userRecord(),"player1":ingame.player1,"player2":ingame.player2}
        return {"message":"Not in Game"}
class PVPGame(Resource):
    @jwt_required()
    def get(self):
        ingame=GameModel.check_if_in_game(current_identity.username)
        if ingame!=None:
            return{"board":ingame.boardTiles,"active":ingame.gameopen,"player1":ingame.player1,"player2":ingame.player2,"status":ingame.gameStatus}
        return GameModel.find_game(current_identity.username)
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

    #change it so that playermove for pvp and pve games are separate
    @jwt_required()
    def put(self):
        data=PlayerMove.parser.parse_args()
        ingame=GameModel.check_if_in_game(current_identity.username)
        user=UserModel.find_by_username(ingame.player1)
        user2=UserModel.find_by_username(ingame.player2)
        if ingame.make_move(data['move'],data['symbol'],current_identity.username):
            game = ingame.check_game_status()
            if game["open"]==True:
                if ingame.pvp== False:               
                    if ingame.cpu_move():
                        game=ingame.check_game_status()
                        if game["open"]==False:
                            if game["status"]==current_identity.username:
                                user.save_win()
                            elif game["status"]=="Tie":
                                user.save_tie()
                            else:
                                user.save_lose()
            else:
                if game["status"]==current_identity.username:
                    user.save_win()
                    if ingame.pvp==True:
                        user2.save_lose()
                elif game["status"]=="Tie":
                    user.save_tie()
                    if ingame.pvp==True:
                        user2.save_tie()
                else:
                    user.save_lose()
                    if ingame.pvp==True:
                        user2.save_win()
        ingame=GameModel.check_if_in_game(current_identity.username)
        return{"board":ingame.boardTiles,"status":ingame.gameStatus,"active":ingame.gameopen,"player1":ingame.player1,"player2":ingame.player2}



