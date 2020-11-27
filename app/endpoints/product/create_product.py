from datetime import datetime

import jwt
from flask import request
from flask_restful import Resource

from app import db
from app.models import Product
from app.views import cloud
from app.endpoints.utils import check_user_session, validate_picture


class CreateProduct(Resource):
    def post(self):
        try:
            user = check_user_session(request)

            if user.store is None:
                raise Exception("You need to create a Store first")

            files = request.files
            upload = {}

            if 'image' in files:
                files['image'].filename = validate_picture(files['image'])

                upload = cloud.uploader.upload(file=files['image'],
                                               use_filename=True,
                                               unique_filename=True,
                                               folder='product')

            product = request.form

            new_product = Product(name=product['name'],
                                  description=product['description'],
                                  price=product['price'],
                                  category=product['category'],
                                  date_added=datetime.now(),
                                  image=upload.get('url', 'null'),
                                  store=user.store,
                                  store_id=user.store.id)

            db.session.add(new_product)
            db.session.commit()

            return {'status': 'ok',
                    'message': 'The product was added successfully',
                    'product': new_product.to_dict(rules=('-comments', '-store', '-likes', '-users'))}, 201
        except jwt.ExpiredSignatureError as e:
            return {'status': 'fail',
                    'message': str(e)}, 401
        except Exception as e:
            return {'status': 'fail',
                    'message': str(e)}, 400
