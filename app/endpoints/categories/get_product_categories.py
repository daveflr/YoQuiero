from app import Category
from flask_restful import Resource


class GetProductCategories(Resource):
    def get(self):
        try:
            categories = Category.query.all()
            return {'status': 'ok',
                    'categories': [category.to_dict(rules=('-products',)) for category in categories]}, 200
        except Exception as e:
            return {'status': 'fail',
                    'message': str(e)}, 400
