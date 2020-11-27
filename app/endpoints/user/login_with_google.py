from flask import request
from flask_restful import Resource

from app.endpoints.utils import check_user_session, validate_picture


class LoginWithGoogle(Resource):
    def post(self):
        pass
