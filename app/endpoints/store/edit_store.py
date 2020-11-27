from flask import request
from flask_restful import Resource

from app import  db
from app.views import cloud
from app.endpoints.utils import check_user_session, validate_picture


class EditStore(Resource):
    def put(self):
        try:
            user = check_user_session(request)

            if user.store is None:
                raise Exception("You need to create a Store first")

            store_id = request.args.get('store_id')

            if store_id is None:
                raise Exception("You must indicate the ID of the Store")

            if user.store.id != int(store_id):
                raise Exception("You dont have permissions to edit this Store")

            files = request.files

            if 'profile_picture' in files:
                files['profile_picture'].filename = validate_picture(files['profile_picture'])

                upload = cloud.uploader.upload(file=files['profile_picture'],
                                               use_filename=True,
                                               unique_filename=True,
                                               folder='store')

                user.store.profile_picture = upload['url']

            if 'background_picture' in files:
                files['background_picture'].filename = validate_picture(files['background_picture'])

                upload = cloud.uploader.upload(file=files['background_picture'],
                                               use_filename=True,
                                               unique_filename=True,
                                               folder='store')

                user.store.background_picture = upload['url']

            user.store.name = request.form.get('name', user.store.name)
            user.store.category = request.form.get('category', user.store.category)
            user.store.description = request.form.get('description', user.store.description)
            user.store.departamento = request.form.get('departamento', user.store.departamento)

            db.session.commit()

            store_dict = user.store.to_dict(rules=('-products', '-user'))
            # store_dict['user'] = user.store.user.to_dict(rules=('-password', '-id', '-comments', '-store', '-likes'))
            # store_dict['products'] = [product.to_dict(rules=('-comments', '-store', '-likes')) for product in
            #                           user.store.products]

            return {'status': 'ok',
                    'message': 'All changes saved',
                    'store': store_dict}, 200
        except Exception as e:
            return {'status': 'fail',
                    'message': str(e)}, 400