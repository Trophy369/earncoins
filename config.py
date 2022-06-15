import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = 'ahundredpercentahundredandtenpercent'
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'earncions@gmail.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = 'from@earncoins.ltd'
    MAIL_SUBJECT_PREFIX = 'Earncoins(AI)bot User'
    # CRYPTOWELL_ADMIN =  os.environ.get('CRYPTOWELL_ADMIN')
    ADMINS = ['earncions@gmail.com']


class ProdConfig(Config):
    pass


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


config = {
    'development': DevConfig,
    'production': ProdConfig,
    'default': DevConfig
}

