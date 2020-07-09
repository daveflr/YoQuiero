import os
import bcrypt
import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()


def encode_auth_token(user_id, username):
    """
    Generates the Auth Token
    """
    try:
        payload = {
            'exp': datetime.utcnow() + timedelta(days=0, seconds=50000),
            'iat': datetime.utcnow(),
            'sub': user_id,
            'name': username
        }

        return jwt.encode(
            payload,
            os.getenv('SECRET'),
            algorithm='HS256'
        )
    except Exception as e:
        return e


def decode_auth_token(token):
    """Check if the Auth token is valid"""
    payload = jwt.decode(token, os.getenv('SECRET'), algorithm='HS256')
    return payload


def generate_password_hash(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)

    return hashed.decode()


def check_password_hash(password, password_hash):
    return bcrypt.checkpw(password.encode(), password_hash.encode())
