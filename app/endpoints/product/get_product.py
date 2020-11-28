from flask import request
from flask_restful import Resource

from app import Product


class GetProduct(Resource):
    def get(self):
        try:
            product_id = request.args.get('product_id')
            product = Product.query.get(product_id)

            product_dict = product.to_dict(rules=('-comments', '-store', '-likes', '-users', '-category'))
            product_dict['comments'] = [comment.to_dict() for comment in product.comments]
            product_dict['store'] = product.store.to_dict(rules=('-products', '-user', '-category', '-departament'))

            return {'status': 'ok',
                    'product': product_dict}, 200
        except AttributeError as e:
            return {'status': 'fail',
                    'message': 'This product does not exists'}, 404
        except Exception as e:
            return {'status': 'fail',
                    'message': str(e)}, 400
