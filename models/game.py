from db import db
from flask import jsonify
import copy
import uuid
from werkzeug.security import generate_password_hash, check_password_hash

class GameModel(db.Model):
    __tablename__="game"

    id = db.Column(db.Integer, primary_key=True)
    player1=db.Column(db.String(50))
    player2=db.Column(db.String(50))
    s1=db.Column(db.String(2))
    s2=db.Column(db.String(2))
    s3=db.Column(db.String(2))
    s4=db.Column(db.String(2))
    s5=db.Column(db.String(2))
    s6=db.Column(db.String(2))
    s7=db.Column(db.String(2))
    s8=db.Column(db.String(2))
    s9=db.Column(db.String(2))
    #add a count of the number of squares that are filled to not have to check if board is full
    #add a column that keeps track of game status so players cant do anything if game status is gameover
    playerturn=db.Column(db.Boolean, default=True)

    def __init__(self,username):
        self.player1=username
        self.player2="CPU"
        self.s1=""
        self.s2=""
        self.s3=""
        self.s4=""
        self.s5=""
        self.s6=""
        self.s7=""
        self.s8=""
        self.s9=""
        self.playerturn=True
    
    def gameBoard(self):
        return[
        self.s1,
        self.s2,
        self.s3,
        self.s4,
        self.s5,
        self.s6,
        self.s7,
        self.s8,
        self.s9]
    
    @classmethod
    def check_if_in_game(cls,username):
        return cls.query.filter_by(player1=username).first()
    def create_game(self,username):
        db.session.add(self)
        db.session.commit()
        gameInfo=GameModel.query.filter_by(player1=username).first()
        return {"message":"Game Started","game_id":gameInfo.id,"board":["","","","","","","","",""]}
    @classmethod
    def leave_game(cls,user_id):
        cls.query.filter_by(player1=user_id).delete()
        db.session.commit()
    @classmethod
    def find_by_id(cls,user_id):
        return cls.query.filter_by(id=user_id).first()
    def make_move(self,move, symbol):
        if self.playerturn==True:
            self.playerturn=False
            if move==1:
                if self.s1!="":
                    return False
                self.s1=symbol
            elif move==2:
                if self.s2!="":
                    return False
                self.s2=symbol
            elif move==3:
                if self.s3!="":
                    return False
                self.s3=symbol
            elif move==4:
                if self.s4!="":
                    return False
                self.s4=symbol
            elif move==5:
                if self.s5!="":
                    return False
                self.s5=symbol
            elif move==6:
                if self.s6!="":
                    return False
                self.s6=symbol
            elif move==7:
                if self.s7!="":
                    return False
                self.s7=symbol
            elif move==8:
                if self.s8!="":
                    return False
                self.s8=symbol
            elif move==9:
                if self.s9!="":
                    return False
                self.s9=symbol
            db.session.commit()
            return True
        return False
    def cpu_move(self):
        if self.playerturn==False:
            self.playerturn=True
            if self.s1=="":
                self.s1="o"
            elif self.s2=="":
                self.s2="o"
            elif self.s3=="":
                self.s3="o"
            elif self.s4=="":
                self.s4="o"
            elif self.s5=="":
                self.s5="o"
            elif self.s6=="":
                self.s6="o"
            elif self.s7=="":
                self.s7="o"
            elif self.s8=="":
                self.s8="o"
            elif self.s9=="":
                self.s9="o"
            db.session.commit()
            return True
        return False
    def check_game_status(self):
        board=[]
        board.append(self.s1)
        board.append(self.s2)
        board.append(self.s3)
        board.append(self.s4)
        board.append(self.s5)
        board.append(self.s6)
        board.append(self.s7)
        board.append(self.s8)
        board.append(self.s9)
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
            return{"winner":"player1"}
        elif found=="o":
            return {"winner":"player2"}
        elif allempty==True:
            return {"winner":"tie"}
        else:
            return{"winner":"none"}

        