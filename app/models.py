from .app import db
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.sql import func


class CartItem(db.Model, SerializerMixin):
    # id = db.Column(db.Integer, primary_key=True)

    # Cart item cart only have a User
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

    # Cart item only have a product
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)

    product = db.relationship('Product', back_populates='users', lazy=False)
    user = db.relationship('User', back_populates='cart_items', lazy=False)
    quantity = db.Column(db.Integer, nullable=False)


class User(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    email = db.Column(db.String, unique=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    password = db.Column(db.Text)

    # User can make many comments
    comments = db.relationship('Comment', back_populates='user', lazy=True)

    # A user can only have a Store
    store = db.relationship('Store', lazy=True, uselist=False, back_populates='user')

    # A user can only have a shopping cart
    cart_items = db.relationship('CartItem', lazy=True, back_populates='user')

    # A User can have many likes
    likes = db.relationship('Like', back_populates='user', lazy=True)


class Store(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    departamento = db.Column(db.String, nullable=False)
    profile_picture = db.Column(db.String, nullable=True)
    background_picture = db.Column(db.String, nullable=True)

    # A store can only have a User
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', back_populates='store')

    # A store can have many products
    products = db.relationship('Product', back_populates='store', lazy=False, cascade='save-update, merge, delete')


class Product(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)

    price = db.Column(db.Float, nullable=False)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', uselist=False, back_populates='products')

    date_added = db.Column(db.DateTime, nullable=False)
    image = db.Column(db.String, nullable=False)

    # A product can have many comments
    comments = db.relationship('Comment', back_populates='product', lazy=True)

    # A product can have many likes
    likes = db.relationship('Like', back_populates='product', lazy=True)

    # A product only have a Store
    store_id = db.Column(db.Integer, db.ForeignKey('store.id'), nullable=False)
    store = db.relationship('Store', back_populates='products')

    # A product can be in a cart of many users
    users = db.relationship('CartItem', back_populates='product', lazy=True)


class Comment(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)

    # A comment only have a User
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', back_populates='comments')

    # A comment only have a Product
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    product = db.relationship('Product', back_populates='comments')

    text = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)


class Like(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    liked_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)

    # A like only have a User
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', back_populates='likes')

    # A like only have a Product
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    product = db.relationship('Product', back_populates='likes')


class Category(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    products = db.relationship("Product", back_populates="category", lazy=True)
