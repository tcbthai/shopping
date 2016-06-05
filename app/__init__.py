from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from config import config
from flask_login import LoginManager
from flask_mail import Mail
import braintree
import os
import jinja2

# class called
basedir = os.path.abspath(os.path.dirname(__file__))
db = SQLAlchemy()
loginmanager = LoginManager()
loginmanager.session_protection = 'strong'
loginmanager.login_view = 'auth.login'
mail = Mail()


def create_app(config_name):
    # Register app and config
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    braintree.Configuration.configure(
        app.config['BT_ENVIRONMENT'],
        app.config['BT_MERCHANT_ID'],
        app.config['BT_PUBLIC_KEY'],
        app.config['BT_PRIVATE_KEY']
    )
    my_loader = jinja2.ChoiceLoader([app.jinja_loader, jinja2.FileSystemLoader('app/static')])
    app.jinja_loader = my_loader

    db.init_app(app)
    loginmanager.init_app(app)
    mail.init_app(app)

    # Register Blueprint
    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    from admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint)
    from before_request_global import before_request_global as global_blueprint
    app.register_blueprint(global_blueprint)
    from payment import payment as payment_blueprint
    app.register_blueprint(payment_blueprint)

    return app
