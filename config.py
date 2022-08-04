import os
from dotenv import load_dotenv
from redislite import Redis

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir,'.env'))


class Config(object):
    SECRET_KEY = 'ahundredpercentahundredandtenpercent'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    # MAIL_USE_SSL = True
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'earncions@gmail.com'
    MAIL_PASSWORD = 'rgrtvmpgjiyaxvgi'
    MAIL_LABEL = 'inbox'
    MAIL_DEFAULT_SENDER = 'from@earncoins.ltd'
    MAIL_SUBJECT_PREFIX = 'Earncoins(AI)bot User'
    # CRYPTOWELL_ADMIN =  os.environ.get('CRYPTOWELL_ADMIN')
    ADMINS = 'earncions@gmail.com'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_RECYCLE = 299

    # Celery configuration
    # CELERY_BROKER_URL = 'redis://localhost:6379/0'
    # CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

    # Create a Redis instance using redislite
    REDIS_DB_PATH = os.path.join('/tmp/my_redis.db')
    rdb = Redis(REDIS_DB_PATH)
    REDIS_SOCKET_PATH = 'redis+socket://%s' % (rdb.socket_file, )

    # Use redislite for the Celery broker
    CELERY_BROKER_URL = REDIS_SOCKET_PATH

    # (Optionally) use redislite for the Celery result backend
    CELERY_RESULT_BACKEND = REDIS_SOCKET_PATH

# class ProdConfig(Config):



# class DevConfig(Config):
#     DEBUG = True
#     SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
#     SQLALCHEMY_TRACK_MODIFICATIONS = False


# config = {
#     'development': DevConfig,
#     'production': ProdConfig,
#     'default': DevConfig
# }

