from flask_restful import Resource,reqparse
from flask_jwt import jwt_required, current_identity
from models.user import UserModel

class UserSignup(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="Field cannot be empty")
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="Field cannot be empty")
    parser.add_argument('email',
                        type=str,
                        required=True,
                        help="Field cannot be empty")
    def post(self):
        data=UserSignup.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return{'message': 'Username is already in use.'}
        if UserModel.find_by_email(data['email']):
            return{'message': 'Email is already in use.'}
        user=UserModel(data['username'],data['password'], data['email'])
        user.save_to_db()

        return{'message': 'User created'}
class UserWin(Resource):
    @jwt_required
    def put(self):
        user=current_identity
        foundUser=UserModel.find_by_email(user.email)
        if foundUser:
            foundUser.save_win()

        return{'message': 'Win Saved'}
class UserLose(Resource):
    @jwt_required
    def put(self):
        user=current_identity
        foundUser=UserModel.find_by_email(user.email)
        if foundUser:
            foundUser.save_lose()

        return{'message': 'Lose Saved'}
class UserTie(Resource):
    @jwt_required
    def put(self):
        user=current_identity
        foundUser=UserModel.find_by_email(user.email)
        if foundUser:
            foundUser.save_tie()

        return{'message': 'Tie Saved'}
class LeaderBoard(Resource):
    @jwt_required
    def get(self):
        return UserModel.leaderBoard()
class UserRecord(Resource):
    @jwt_required
    def get(self):
        user=current_identity
        foundUser=UserModel.find_by_email(user.email)
        if foundUser:
            return foundUser.userRecord()
class Test(Resource):
    def put(self):
        return {"hey":"hello"}
        
