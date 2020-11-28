import jwt
from flask import request
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from app import db
from app.models import Store
from app.endpoints.utils import check_user_session


class CreateStore(Resource):
    def post(self):
        try:
            user = check_user_session(request)

            store = request.json

            new_store = Store(name=store['name'],
                              category_id=store['category'],
                              description=store['description'],
                              departament_id=int(store['departament']),
                              email=store['email'],
                              phone_number=store['phone_number'],
                              user=user,
                              user_id=user.id)
            # new_store.user_id = user.id

            if not new_store:
                raise Exception('Failed to create a new Store')

            db.session.add(new_store)
            db.session.commit()

            return {'status': 'ok',
                    'store': new_store.to_dict(rules=('-user', '-user_id', '-products', '-category', '-departament')),
                    'user': user.to_dict(rules=('-password', '-id', '-comments', '-store', '-likes'))}, 201
        except jwt.ExpiredSignatureError as e:
            return {'status': 'fail',
                    'message': str(e)}, 401
        except IntegrityError as e:
            return {'status': 'fail', 'message': 'A user can only have a store'}, 400
        except Exception as e:
            print(str(e))
            return {'status': 'fail', 'message': str(e)}, 400
