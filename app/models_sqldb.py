from app import db, loginmanager
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app, url_for, render_template
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin
import datetime


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    product = db.relationship('Product', backref='category', cascade="all, delete-orphan")

    @staticmethod
    def insert_categories():
        categories = ['photography', 'photoshop', 'camera']
        for c in categories:
            category = Category.query.filter_by(name=c).first()
            if category is None:
                print c
                category = Category(name=c)
                db.session.add(category)
        db.session.commit()


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password_hash = db.Column(db.String(255))
    history = db.relationship('History', backref='buyer', cascade="all, delete-orphan")
    isAdmin = db.Column(db.Boolean, default=False)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if not self.isAdmin:
            if self.email == current_app.config['FLASKY_ADMIN']:
                self.isAdmin = True
            if not self.isAdmin:
                self.isAdmin = False

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'token_id': self.id})

    @staticmethod
    def get_token_id(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return data.get('token_id')

    @loginmanager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)


class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    product_code = db.Column(db.String(255))
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    image = db.Column(db.String(255))
    description = db.Column(db.Text)
    name = db.Column(db.String(255))
    stock = db.Column(db.Integer)
    price = db.Column(db.Integer)
    detail = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))


class History(db.Model):
    __tablename__ = 'histories'
    id = db.Column(db.Integer, primary_key=True)
    product_code = db.Column(db.String)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    quantity = db.Column(db.Integer)
    user_id= db.Column(db.Integer, db.ForeignKey('users.id'))
