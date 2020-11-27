from flask import request
from flask_restful import Resource

from app import db
from app.models import User
from app.auth import generate_password_hash, encode_auth_token


class SignUp(Resource):
    def post(self):
        try:
            data = request.form
            new_user = User(
                username=data.get('username', None),
                email=data['email'],
                name=data['name'],
                last_name=data['last_name'],
                password=generate_password_hash(
                    data.get('password', None)
                )
            )
            db.session.add(new_user)
            db.session.commit()

            return {'status': 'ok',
                    'user': new_user.to_dict(rules=('-password', '-id', '-comments', '-store', '-likes')),
                    'token': encode_auth_token(new_user.id, new_user.email).decode()}, 201
        except Exception as e:
            print(str(e))
            return {'status': 'fail', 'message': str(e)}, 500
