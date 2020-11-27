from datetime import datetime
from app.auth import decode_auth_token
from app.models import User


def check_user_session(request_):
    auth_header = request_.headers.get('Authorization')

    if auth_header is None:
        raise Exception('You must indicate Authorization token. The auth token is missing')

    auth_token = auth_header.split(" ")[1]

    user_payload = decode_auth_token(auth_token)

    user = User.query.get(user_payload['sub'])
    if not user:
        raise Exception('Username not found')

    return user


def allowed_file_types(content_type):
    file_types = ['image/jpg', 'image/png', 'image/jpeg']
    return content_type in file_types


def validate_picture(picture):
    if picture.filename == '':
        raise Exception('Filename of profile picture must not be empty')

    if not allowed_file_types(picture.content_type):
        raise Exception('Only jpg and png images are supported')

    file_extension = picture.filename.rsplit(".", 1)[1].lower()
    picture.filename = datetime.now().strftime("%Y%m%d-%H%M%S%f.") + file_extension

    return picture.filename
