import jwt
from flask import request
from flask_restful import Resource

from app import db
from app.models import Product, Like
from app.endpoints.utils import check_user_session


class LikeProduct(Resource):
    def post(self):
        try:
            user = check_user_session(request)
            product_id = request.args.get('product_id')

            product = Product.query.get(product_id)

            if product is None:
                raise Exception("Product is missing")

            if product.id not in [like.product_id for like in user.likes]:
                # add like
                like = Like(user_id=user.id, product_id=product.id)

                db.session.add(like)
                db.session.commit()

                return {'status': 'ok',
                        'message': 'Product liked'}, 201
            else:
                # remove like
                like = Like.query.filter(Like.user_id == user.id, Like.product_id == product_id).first()

                db.session.delete(like)
                db.session.commit()

                return {'status': 'ok',
                        'message': 'Product disliked'}, 201

        except jwt.ExpiredSignatureError as e:
            return {'status': 'fail',
                    'message': str(e)}, 401
        except Exception as e:
            return {'status': 'fail',
                    'message': str(e)}, 400
