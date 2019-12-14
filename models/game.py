from db import db
from flask import jsonify
import copy
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import or_
from sqlalchemy.orm.attributes import flag_modified
from models.user import UserModel

class GameModel(db.Model):
    __tablename__="game"

    id = db.Column(db.Integer, primary_key=True)
    player1=db.Column(db.String(50))
    pvp=db.Column(db.Boolean, default=True)
    player2=db.Column(db.String(50))
    boardTiles=db.Column(db.ARRAY(db.String(2)))
    gameopen=db.Column(db.Boolean, default=True)
    gameStatus=db.Column(db.String(70))

    def __init__(self,username,gametype,secondPlayer):
        self.player1=username
        self.player2=secondPlayer
        self.boardTiles=["","","","","","","","",""]
        self.gameopen=True
        if gametype=="pvp":
            self.pvp=True
            self.gameStatus=username
        else:
            self.pvp=False
            self.gameStatus="Waiting for opponent"
    @classmethod
    def check_if_in_game(cls,username):
        return cls.query.filter(or_(cls.player1==username, cls.player2==username)).first()
    @classmethod
    def leave_game(cls,user_id):
        games=cls.query.filter(or_(cls.player1==user_id, cls.player2==user_id)).delete()
        db.session.commit()
    @classmethod
    def find_by_id(cls,user_id):
        return cls.query.filter_by(id=user_id).first()
    def make_move(self,move,symbol,username):
        if username==self.gameStatus:    
            if self.boardTiles[move-1]!="":
                return False
            if username==self.player1:
                self.boardTiles[move-1]="x"
                self.gameStatus=self.player2
                flag_modified(self, 'boardTiles')
            else:
                self.boardTiles[move-1]="o"
                self.gameStatus=self.player1
                flag_modified(self, 'boardTiles')
            db.session.commit()
            return True
        return False
    @classmethod
    def find_game(cls,user_id):
        game= cls.query.filter(cls.player1 != user_id).filter(cls.player2=="").filter_by(pvp=True).first()
        if game==None:
            game=GameModel(user_id,True,"")
            db.session.add(game)
            db.session.commit()
            return{"message":"Game Start", "status":game.gameStatus,"active":game.gameopen,"board":game.boardTiles,"player1":game.player1,"player2":game.player2}
        else:
            game.player2=user_id
            db.session.commit()
            return{"message":"Game Continued", "status":game.gameStatus,"active":game.gameopen,"board":game.boardTiles,"player1":game.player1,"player2":game.player2}
    def cpu_move(self):
        if self.gameStatus=="CPU":
            for num, tile in enumerate(self.boardTiles):
                if tile=="":
                    self.boardTiles[num]="o"
                    self.gameStatus=self.player1
                    flag_modified(self, 'boardTiles')
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
            self.gameStatus=self.player1
            db.session.commit()
        elif found=="o":
            self.gameopen=False
            self.gameStatus=self.player2
            db.session.commit()
        elif allempty==True:
            self.gameopen=False
            self.gameStatus="Tie"
            db.session.commit()
        return{"status":self.gameStatus,"open":self.gameopen}

        