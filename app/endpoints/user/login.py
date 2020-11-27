from flask import request
from flask_restful import Resource

from app.models import User
from app.auth import encode_auth_token, check_password_hash


class Login(Resource):
    def post(self):
        try:
            data = request.form
            user = User.query.filter_by(email=data['email']).first()

            if user is None:
                raise Exception('Invalid username or email')

            if check_password_hash(data['password'], user.password):
                token = encode_auth_token(user.id, user.username).decode()
                user_ = user.to_dict(
                    rules=(
                        '-password', '-id', '-comments', '-store', '-likes', '-cart_items'
                    ))
                return {'status': 'ok',
                        'user': user_,
                        'token': token}, 200
            else:
                raise Exception('Invalid password or username')
        except Exception as e:
            return {'status': 'fail', 'message': str(e)}, 401
