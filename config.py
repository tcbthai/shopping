import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or "VSFNN8L1N"
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'The Presence <chuvi0902@gmail.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN') or "chuvi0902@gmail.com"
    FLASKY_POSTS_PER_PAGE = 10
    FLASKY_COMMENTS_PER_PAGE = 15

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
    BT_ENVIRONMENT = 'sandbox'
    BT_MERCHANT_ID = 'zv9nzjjn5kw2xtdm'
    BT_PUBLIC_KEY = 'dwxjn4pjnkdkmshs'
    BT_PRIVATE_KEY = '12fcef637af5e9049cd260e6c2883c0c'
    APP_SECRET_KEY = 'Vu1781991'


class ProductionConfig(Config):
    pass


config = {
    'Dev': DevelopmentConfig,
    'Pro': ProductionConfig,
    'default': DevelopmentConfig
}
