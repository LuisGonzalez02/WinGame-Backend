from db import db
from flask import jsonify
import uuid
from werkzeug.security import generate_password_hash, check_password_hash

class UserModel(db.Model):
    __tablename__="user"

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(50), unique=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(80))
    wins=db.Column(db.Integer)
    loses=db.Column(db.Integer)
    ties=db.Column(db.Integer)

    def __init__(self,username,password,email):
        hashed_password = generate_password_hash(password)
        self.public_id=str(uuid.uuid4())
        self.email=email
        self.password=hashed_password
        self.username=username
        self.wins=0
        self.loses=0
        self.ties=0
    def json(self):
        return{username: self.username}
    
    @classmethod
    def find_by_email(cls,email):
        return cls.query.filter_by(email=email).first()
    @classmethod
    def find_by_username(cls,username):
        return cls.query.filter_by(username=username).first()
    @classmethod
    def find_by_id(cls,user_id):
        return cls.query.filter_by(id=user_id).first()
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
    def save_win(self):
        self.wins+=1
        db.session.commit()
    def save_lose(self):
        self.loses+=1
        db.session.commit()
    def save_tie(self):
        self.ties+=1
        db.session.commit()
    @classmethod
    def leaderBoard(cls):
        leaders = cls.query.order_by(cls.wins.desc()).all()
        if not leaders:
            return jsonify({'message' : 'No user found!'})
        output=[]
        for leader in leaders:
            user_data = {}
            user_data['name'] = leader.username
            user_data['wins'] = leader.wins
            user_data['loses'] = leader.loses
            user_data['ties'] = leader.ties
            output.append(user_data)

        return jsonify({'leaders' : output})
    def userRecord(self):
        user_record = {}
        user_record['wins'] = self.wins
        user_record['loses'] = self.loses
        user_record['ties'] = self.ties
        return {self.username:user_record}




    