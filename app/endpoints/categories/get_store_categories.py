from app import StoreCategory
from flask_restful import Resource


class GetStoreCategories(Resource):
    def get(self):
        try:
            categories = StoreCategory.query.all()
            return {'status': 'ok',
                    'categories': [category.to_dict(rules=('-store_categories',)) for category in categories]}, 200
        except Exception as e:
            return {'status': 'fail',
                    'message': str(e)}, 400
