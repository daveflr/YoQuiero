from .app import db
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.sql import func


class User(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    password = db.Column(db.Text, nullable=False)

    # User can make many comments
    comments = db.relationship('Comment', back_populates='user', lazy=True)

    # A user can only have a Store
    store = db.relationship('Store', lazy=True, uselist=False, back_populates="user")

    # A User can have many likes
    likes = db.relationship('Like', back_populates="user", lazy=True)


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
    user = db.relationship("User", back_populates="store")

    # A store can have many products
    products = db.relationship('Product', backref='store', lazy=False, cascade="save-update, merge, delete")


class Product(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)

    price = db.Column(db.Float, nullable=False)

    category = db.Column(db.String, nullable=False)
    date_added = db.Column(db.DateTime, nullable=False)
    likes_count = db.Column(db.Integer, nullable=False, default=0)
    image = db.Column(db.String, nullable=False)

    # A product can have many comments
    comments = db.relationship('Comment', back_populates='product', lazy=True)

    # A Product can have many likes
    likes = db.relationship('Like', back_populates='product', lazy=True)

    # A product belongs to a Store
    store_id = db.Column(db.Integer, db.ForeignKey('store.id'), nullable=False)


class Comment(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship("User", lazy=True, back_populates="comments")

    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    product = db.relationship("Product", lazy=True, back_populates="comments")

    text = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)


class Like(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)

    # A like can only have a User
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship("User", lazy=True, uselist=False, back_populates="likes")

    # A like can only have a Product
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    product = db.relationship("Product", lazy=True, uselist=False, back_populates="likes")

    liked_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
