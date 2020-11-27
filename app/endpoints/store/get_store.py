from flask import request
from flask_restful import Resource

from app import Store


class GetStore(Resource):
    def get(self):
        try:
            store_id = request.args.get('store_id')
            if store_id is None:
                raise Exception("You must indicate the ID of the Store")

            store = Store.query.get(store_id)

            store_dict = store.to_dict(rules=('-products', '-user'))
            store_dict['user'] = store.user.to_dict(rules=('-password', '-id', '-comments', '-store', '-likes'))
            store_dict['products'] = [product.to_dict(rules=('-comments', '-store', '-likes')) for product in
                                      store.products]

            return {'status': 'ok',
                    'store': store_dict}, 200
        except AttributeError as e:
            return {'status': 'fail',
                    'message': 'This store does not exists'}, 404
        except Exception as e:
            return {'status': 'fail',
                    'message': str(e)}, 400
