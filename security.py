from werkzeug.security import generate_password_hash, check_password_hash, safe_str_cmp
from models.user import UserModel

def authenticate(email, password):
    user=UserModel.find_by_email(email)
    if check_password_hash(user.password, password):
        return user

def identity(payLoad):
    user_email=payload['identity']
    return UserModel.find_by_email(user_email)