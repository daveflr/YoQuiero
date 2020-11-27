import jwt
from flask import request
from flask_restful import Resource

from app import db, Product, CartItem
from app.endpoints.utils import check_user_session


class AddToCart(Resource):
    def post(self):
        try:
            user = check_user_session(request)

            product_id = request.args.get('product_id')
            quantity = request.args.get('quantity')

            product = Product.query.get(product_id)

            if product is None:
                raise Exception("Product is missing")

            for item in user.cart_items:
                if product == item.product:
                    return {'status': 'ok',
                            'message': 'This product is already in you shopping cart'}, 200

            cart_item = CartItem(quantity=quantity)
            cart_item.user = user
            cart_item.product = product

            user.cart_items.append(cart_item)

            db.session.commit()

            return {'status': 'ok',
                    'message': 'This product was added to you shopping cart'}, 201
        except jwt.ExpiredSignatureError as e:
            return {'status': 'fail',
                    'message': str(e)}, 401
        except Exception as e:
            return {'status': 'fail',
                    'message': str(e)}, 400
