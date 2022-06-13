import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    EARNCOINS_MAIL_SENDER = "Earncoins <countliason@gmail.com>"
    EARNCOINS_MAIL_SUBJECT_PREFIX = '[Earncoins Limited]'
    # CRYPTOWELL_ADMIN =  os.environ.get('CRYPTOWELL_ADMIN')
    ADMINS = ['earncions@gmail.com']


class ProdConfig(Config):
    pass


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


