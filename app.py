from flask import Flask
from flask_restful import Api
import os
from flask_jwt import jwt

from security import authenticate,identity
from resources.user import UserSignup,

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['PROPAGATE_EXCEPTIONS']=True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
api=Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

jwt=JWT(app, authenticate, identity)

api.add_resource(UserSignup, '/signup')


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000,debug=True)