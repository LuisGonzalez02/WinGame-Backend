from flask_restful import Resource,reqparse
from flask_jwt import jwt_required, current_identity
from flask import jsonify
from models.game import GameModel
from models.user import UserModel

class Game(Resource):
    @jwt_required()
    def get(self):
        ingame=GameModel.check_if_in_game(current_identity.username)
        if ingame["game"]!=None:
            board=ingame["game"].boardTiles
            return{"message": "Username already in game","game_id":ingame["game"].id,"board":board,"active":ingame["game"].gameopen,"player1":current_identity.username,"player2":"CPU"}
        foundUser=GameModel(current_identity.username,"solo","CPU")
        return foundUser.create_game(current_identity.username,False)
    @jwt_required()
    def delete(self):
        info= GameModel.check_if_in_game(current_identity.username)
        if(info["game"]!=None):
            GameModel.leave_game(current_identity.username)
            return {'message':"You have left the game"}
class PVPCheckIfMove(Resource):
    @jwt_required()
    def get(self):
        ingame=GameModel.check_if_in_game(current_identity.username)
        user=UserModel.find_by_username(current_identity.username)
        if ingame["game"] !=None:
            return {"message": "User in Game","board":ingame['game'].boardTiles,"record":user.userRecord(),"player1":current_identity.username,"player2":ingame['player2']}
        return {"message":"Not in Game"}
class PVPGame(Resource):
    @jwt_required()
    def get(self):
        ingame=GameModel.check_if_in_game(current_identity.username)
        if ingame["game"]!=None:
            board=ingame["game"].boardTiles
            return{"message": "Username already in game","game_id":ingame["game"].id,"board":board,"active":ingame["game"].gameopen}
        foundUser=GameModel(current_identity.username,"pvp","")
        return foundUser.find_game(current_identity.username)

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

    #change it so that playermove for pvp and pve gamer are separate
    @jwt_required()
    def put(self):
        data=PlayerMove.parser.parse_args()
        ingame=GameModel.check_if_in_game(current_identity.username)
        user=UserModel.find_by_username(current_identity.username)
        user2=UserModel.find_by_username(ingame['player2'])
        if ingame["game"]!=None:
            board=ingame["game"].boardTiles
            if ingame["game"].make_move(data['move'],data['symbol'],user.username):
                game=ingame["game"].check_game_status()
                if game["open"]==True:
                    if ingame["game"].pvp== False:               
                        if ingame["game"].cpu_move():
                            board=ingame["game"].boardTiles
                            game=ingame["game"].check_game_status()
                            if game["open"]==True:
                                return{"Game Status":"Still going","message":"Move has been made","board":board}
                            if game["status"]==current_identity.username:
                                user.save_win()
                                return{"Game Status":"Game Won","message":"Move has been made","board":board}
                            elif game["status"]=="Tie":
                                user.save_tie()
                                return{"Game Status":"Tie","message":"Move has been made","board":board}
                            else:
                                user.save_lose()
                                return{"Game Status":"Game Lostwaffa","message":"Move has been made","board":board,"info":game["open"],"game status":game["status"]}
                        return {"Game Status":"Still going","message":"Not CPU Turn","board":board}
                    else:
                        board=ingame["game"].boardTiles
                        return {"Game Status":"Still going","board":board,"Game":"PVP"}
                else:
                    board=ingame["game"].boardTiles
                    if game["status"]==current_identity.username:
                        user.save_win()
                        if ingame["game"].pvp==True:
                            user2.save_lose()
                        return{"Game Status":"Game Won","message":"Move has been made","board":board}
                    elif game["status"]=="Tie":
                        user.save_tie()
                        if ingame["game"].pvp==True:
                            user2.save_tie()
                        return{"Game Status":"Tie","message":"Move has been made","board":board}
                    else:
                        user.save_lose()
                        if ingame["game"].pvp==True:
                            user2.save_win()
                        return{"Game Status":"Game Losaaaaaaaat","message":"Move has been made","board":board}
            return {"message":"Not Player Turn/Space already used","Game Status":"Still going","board":board}
        return{"message":"User not in game","Game Status":"Still going","board":["","","","","","","","",""]}
class CPUMove(Resource):
    @jwt_required()
    def put(self):
        ingame=GameModel.check_if_in_game(current_identity.username)
        if info["game"]!=None:
            if ingame["game"].cpu_move():
                return {"message":"Move has been made"}
            return {"message":"Not CPU Turn"}
        return{"message":"User not in game"}



