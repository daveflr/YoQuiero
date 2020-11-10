import cloudinary as cloud
from cloudinary import uploader
from flask_restful import Resource
from flask import request
from .app import api, db, app
from .models import User, Store, Product, Comment, Like, CartItem
from .auth import *
from dotenv import load_dotenv
from sqlalchemy.exc import IntegrityError

load_dotenv()

cloud.config.update = ({
    'cloud_name': os.environ.get('CLOUDINARY_CLOUD_NAME'),
    'api_key': os.environ.get('CLOUDINARY_API_KEY'),
    'api_secret': os.environ.get('CLOUDINARY_API_SECRET')
})


class SignUp(Resource):
    def post(self):
        try:
            data = request.form
            print(request)
            print(data)
            new_user = User(username=data['username'],
                            email=data['email'],
                            name=data['name'],
                            last_name=data['last_name'],
                            password=generate_password_hash(data['password']))
            db.session.add(new_user)
            db.session.commit()

            return {'status': 'ok',
                    'user': new_user.to_dict(rules=('-password', '-id', '-comments', '-store', '-likes')),
                    'token': encode_auth_token(new_user.id, new_user.username).decode()}, 201
        except Exception as e:
            print(str(e))
            return {'status': 'fail', 'message': str(e)}, 500


class Login(Resource):
    def post(self):
        try:
            data = request.form
            print(request)
            print(data)
            user = User.query.filter_by(email=data['email']).first()

            if user is None:
                raise Exception('Invalid username or email')

            if check_password_hash(data['password'], user.password):
                token = encode_auth_token(user.id, user.username).decode()

                return {'status': 'ok',
                        'user': user.to_dict(rules=('-password', '-id', '-comments', '-store', '-likes')),
                        'token': token}, 200
            else:
                raise Exception('Invalid password or username')
        except Exception as e:
            return {'status': 'fail', 'message': str(e)}, 401


class Logout(Resource):
    def post(self):
        try:
            pass
        except Exception as e:
            pass


class CreateStore(Resource):
    def post(self):
        try:
            user = check_user_session(request)

            store = request.json

            new_store = Store(name=store['name'],
                              category=store['category'],
                              description=store['description'],
                              departamento=store['departamento'],
                              user=user,
                              user_id=user.id)
            # new_store.user_id = user.id

            if not new_store:
                raise Exception('Failed to create a new Store')

            db.session.add(new_store)
            db.session.commit()

            return {'status': 'ok',
                    'store': new_store.to_dict(rules=('-user', '-user_id', '-products')),
                    'user': user.to_dict(rules=('-password', '-id', '-comments', '-store', '-likes'))}, 201
        except jwt.ExpiredSignatureError as e:
            return {'status': 'fail',
                    'message': str(e)}, 401
        except IntegrityError as e:
            return {'status': 'fail', 'message': 'A user can only have a store'}, 400
        except Exception as e:
            print(str(e))
            return {'status': 'fail', 'message': str(e)}, 400


class GetStore(Resource):
    def get(self, store_id):
        try:
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

            product = request.json

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
                    'product': new_product.to_dict(rules=('-comments', '-store', '-likes'))}, 201
        except jwt.ExpiredSignatureError as e:
            return {'status': 'fail',
                    'message': str(e)}, 401
        except Exception as e:
            return {'status': 'fail',
                    'message': str(e)}, 400


class EditProduct(Resource):
    def put(self, product_id):
        try:
            user = check_user_session(request)

            if user.store is None:
                raise Exception("You need to create a Store first")

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

            product.name = request.json.get('name', product.name)
            product.description = request.json.get('description', product.description)
            product.price = float(request.json.get('price', product.price))
            product.category = request.json.get('category', product.category)

            db.session.commit()

            return {'status': 'ok',
                    'message': 'All changes saved'}, 200
        except Exception as e:
            return {'status': 'fail',
                    'message': str(e)}, 400


class GetProduct(Resource):
    def get(self, product_id):
        try:
            product = Product.query.get(product_id)

            product_dict = product.to_dict(rules=('-comments', '-store', '-likes'))
            product_dict['comments'] = [comment.to_dict() for comment in product.comments]
            product_dict['store'] = product.store.to_dict(rules=('-products', '-user'))

            return {'status': 'ok',
                    'store': product_dict}, 200
        except AttributeError as e:
            return {'status': 'fail',
                    'message': 'This product does not exists'}, 404
        except Exception as e:
            return {'status': 'fail',
                    'message': str(e)}, 400


class EditStore(Resource):
    def put(self, store_id):
        try:
            user = check_user_session(request)

            if user.store is None:
                raise Exception("You need to create a Store first")

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

            user.store.name = request.json.get('name', user.store.name)
            user.store.category = request.json.get('category', user.store.category)
            user.store.description = request.json.get('description', user.store.description)
            user.store.departamento = request.json.get('departamento', user.store.departamento)

            db.session.commit()

            return {'status': 'ok',
                    'message': 'All changes saved'}, 200
        except Exception as e:
            return {'status': 'fail',
                    'message': str(e)}, 400


class LikeProduct(Resource):
    def post(self, product_id):
        try:
            user = check_user_session(request)
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


class AddToCart(Resource):
    def post(self, product_id, quantity):
        try:
            user = check_user_session(request)
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


def check_user_session(request_):
    auth_header = request_.headers.get('Authorization')

    if auth_header is None:
        raise Exception('You must indicate Authorization token. The auth token is missing')

    auth_token = auth_header.split(" ")[1]

    user_payload = decode_auth_token(auth_token)

    user = User.query.get(user_payload['sub'])
    if not user:
        raise Exception('Username not found')

    return user


def allowed_file_types(content_type):
    file_types = ['image/jpg', 'image/png', 'image/jpeg']
    return content_type in file_types


def validate_picture(picture):
    if picture.filename == '':
        raise Exception('Filename of profile picture must not be empty')

    if not allowed_file_types(picture.content_type):
        raise Exception('Only jpg and png images are supported')

    file_extension = picture.filename.rsplit(".", 1)[1].lower()
    picture.filename = datetime.now().strftime("%Y%m%d-%H%M%S%f.") + file_extension

    return picture.filename


# ENDPOINTS
api.add_resource(SignUp, '/api/signup')
api.add_resource(Login, '/api/login')
# api.add_resource(Logout, '/api/logout')
api.add_resource(CreateStore, '/api/createStore')
api.add_resource(GetStore, '/api/getStore/<string:store_id>')
api.add_resource(EditStore, '/api/editStore/<string:store_id>')
api.add_resource(CreateProduct, '/api/createProduct')
api.add_resource(EditProduct, '/api/editProduct/<string:product_id>')
api.add_resource(GetProduct, '/api/getProduct/<string:product_id>')
api.add_resource(LikeProduct, '/api/likeProduct/<string:product_id>')
api.add_resource(AddToCart, '/api/addToCart/<string:product_id>/<int:quantity>')
