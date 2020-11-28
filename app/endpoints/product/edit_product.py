import os
from flask import request
from flask_restful import Resource
from cloudinary import uploader
import cloudinary as cloud

from app import db
from app.models import Product, Category
from app.endpoints.utils import check_user_session, validate_picture

cloud.config.update = ({
    'cloud_name': os.environ.get('CLOUDINARY_CLOUD_NAME'),
    'api_key': os.environ.get('CLOUDINARY_API_KEY'),
    'api_secret': os.environ.get('CLOUDINARY_API_SECRET')
})


class EditProduct(Resource):
    def put(self):
        try:
            user = check_user_session(request)

            if user.store is None:
                raise Exception("You need to create a Store first")

            product_id = request.args.get('product_id')

            product = Product.query.get(int(product_id))

            if product not in user.store.products:
                raise Exception("This product does not exists")

            image = request.files

            if 'image' in image:
                image['image'].filename = validate_picture(image['image'])

                upload = cloud.uploader.upload(file=image['image'],
                                               use_filename=True,
                                               unique_filename=True,
                                               folder='product')
                product.image = upload['url']

            new_product = request.form
            new_category = Category.query.get(int(new_product.get('category')))
            product.name = new_product.get('name', product.name)
            product.description = new_product.get('description', product.description)
            product.price = float(new_product.get('price', product.price))
            product.category = new_category

            db.session.commit()

            return {'status': 'ok',
                    'message': 'All changes saved',
                    'product': product.to_dict(rules=('-comments', '-store', '-likes', '-users', '-category'))}, 200
        except Exception as e:
            return {'status': 'fail',
                    'message': str(e)}, 400
