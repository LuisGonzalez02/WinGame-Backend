from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_heroku import Heroku


db = SQLAlchemy()
heroku=Heroku()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATION']=False
   

    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    #app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')

    
    heroku.init_app(app)
    db.init_app(app)

    from api.views import main
    app.register_blueprint(main)

    return app