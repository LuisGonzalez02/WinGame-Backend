from werkzeug.security import check_password_hash, safe_str_cmp
from models.user import UserModel
from flask import jsonify

def authenticate(username, password):
    user=UserModel.find_by_username(username)
    if user and check_password_hash(user.password, password):
        return user

def identity(payload):
    user_id=payload['identity']
    return UserModel.find_by_id(user_id)