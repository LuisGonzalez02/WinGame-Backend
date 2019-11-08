from db import db
from flask import jsonify
import copy
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import or_
from models.user import UserModel

class GameModel(db.Model):
    __tablename__="game"

    id = db.Column(db.Integer, primary_key=True)
    player1=db.Column(db.String(50))
    pvp=db.Column(db.Boolean, default=True)
    player2=db.Column(db.String(50))
    boardTiles=db.Column(db.ARRAY(db.String(2)))
    gameopen=db.Column(db.Boolean, default=True)
    #add a count of the number of squares that are filled to not have to check if board is full
    #add a column that keeps track of game status so players cant do anything if game status is gameover
    playerturn=db.Column(db.Boolean, default=True)

    def __init__(self,username,gametype,cpu):
        self.player1=username
        self.player2=cpu
        self.boardTiles=["","","","","","","","",""]
        self.playerturn=True
        self.gameopen=True
        if gametype=="pvp":
            self.pvp=True
        else:
            self.pvp=False
    
    
    @classmethod
    def check_if_in_game(cls,username):
        position=None
        player=cls.query.filter_by(player1=username).first()
        if player==None:
            player=cls.query.filter_by(player2=username).first()
            if player:
                position=2
        else:
            position=1
        return {"position":position,"info":player}
    def check_turn(self,position,username):
        val=False
        if self.playerturn==True and position==1:
            val= True
        elif self.playerturn==True and position==2:
            val =False
        elif self.playerturn==False and position==1:
            val= False
        elif self.playerturn==False and position==2:
            val= True
        else:
            val=False
        p1=None
        p2=None
        if position==1:
            p1=self.player1
            p2=self.player2
        else:
            p1=self.player2
            p2=self.player1
        user=UserModel.find_by_username(username)
        statline=None
        status=self.check_game_status()
        if status["winner"]=="none":
            statline="Still going"
        elif status["winner"]=="player1" and position==1:
            statline="Game Won"
        elif status["winner"]=="player1" and position==2:
            statline="Game Lost"
        elif status["winner"]=="player2" and position==1:
            statline="Game Lost"
        elif status["winner"]=="player2" and position==2:
            statline="Game Won"
        elif status["winner"]=="tie":
            statline="Tie"
        return{"status":val,"board":self.boardTiles, "record":user.userRecord(),"player1":p1,"player2":p2,"Game Status":statline}
    def create_game(self,username,pvpType):
        self.pvp=pvpType
        db.session.add(self)
        db.session.commit()
        gameInfo=GameModel.query.filter_by(player1=username).first()
        return {"message":"Game Started","game_id":gameInfo.id,"board":["","","","","","","","",""],"active":gameInfo.gameopen,"player1":gameInfo.player1,"player2":gameInfo.player2}
    @classmethod
    def leave_game(cls,user_id):
        games=cls.query.filter(or_(cls.player1==user_id, cls.player2==user_id)).delete()
        db.session.commit()
    @classmethod
    def find_game(cls,user_id):
        game= cls.query.filter(cls.player1 != user_id).filter(cls.player2=="").filter_by(pvp=True).first()
        if game==None:
            user=GameModel(user_id,True,"")
            return user.create_game(user_id,True)
        else:
            game.player2=user_id
            db.session.commit()
            return{"message":"Game Started", "game_id": game.id,"board":game.boardTiles,"player1":game.player1,"player2":game.player2}

    @classmethod
    def find_by_id(cls,user_id):
        return cls.query.filter_by(id=user_id).first()
    def make_move(self,move, symbol,position,username):
        turn=self.check_turn(position,username)
        if turn["status"]:    
            self.playerturn= not self.playerturn
            if self.boardTiles[move-1]!="":
                return False
            if position==1:
                self.boardTiles[move-1]=="x"
            else:
                self.boardTiles[move-1]=="0"
            db.session.commit()
            return True
        return False
    def cpu_move(self):
        if self.playerturn==False:
            self.playerturn=True
            for tile in self.boardTiles:
                if tile=="":
                    tile="0"
                    break
            db.session.commit()
            return True
        return False
    def check_game_status(self):
        board=self.boardTiles
        found = None
        i = 0
        while i < 9:
            if board[i]==board[i+1]and board[i+1]==board[i+2]and board[i]!="":
                found=board[i]
            i += 3
        i=0
        while i < 3:
            if board[i]==board[i+3]and board[i+3]==board[i+6]and board[i]!="":
                found=board[i]
            i += 1
        i = 0
        allempty=True
        while i < 9:
            if board[i]=="":
                allempty=False
            i += 1
        if board[0]==board[4]and board[4]==board[8]and board[0]!="":
            found=board[0]
        if board[2]==board[4]and board[4]==board[6]and board[2]!="":
            found=board[2]
        if found=="x":
            self.gameopen=False
            db.session.commit()
            return{"winner":"player1"}
        elif found=="o":
            self.gameopen=False
            db.session.commit()
            return {"winner":"player2"}
        elif allempty==True:
            self.gameopen=False
            db.session.commit()
            return {"winner":"tie"}
        else:
            return{"winner":"none"}

        