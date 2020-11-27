import os
import cloudinary as cloud
from app import api
from dotenv import load_dotenv
from app.endpoints import *

load_dotenv()

cloud.config.update = ({
    'cloud_name': os.environ.get('CLOUDINARY_CLOUD_NAME'),
    'api_key': os.environ.get('CLOUDINARY_API_KEY'),
    'api_secret': os.environ.get('CLOUDINARY_API_SECRET')
})

# ENDPOINTS
api.add_resource(SignUp, '/api/signup')
api.add_resource(Login, '/api/login')
# api.add_resource(Logout, '/api/logout')
api.add_resource(CreateStore, '/api/createStore')
api.add_resource(GetStore, '/api/getStore')
api.add_resource(EditStore, '/api/editStore')
api.add_resource(CreateProduct, '/api/createProduct')
api.add_resource(EditProduct, '/api/editProduct')
api.add_resource(GetProduct, '/api/getProduct')
api.add_resource(LikeProduct, '/api/likeProduct')
api.add_resource(AddToCart, '/api/addToCart')
