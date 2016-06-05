from . import before_request_global
from flask import g
from app.models_sqldb import Category


@before_request_global.before_app_request
def before_request():
    g.category_list = Category.query.all()
