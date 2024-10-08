import os
from flask import Flask, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from flask_fontawesome import FontAwesome
from flask_admin import Admin, expose, BaseView, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib import sqla
from flask_bootstrap import Bootstrap
from flask_login import current_user
from config import Config
from flask_celery import Celery

from webapp.decorators import has_role


db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
fa = FontAwesome()
bootstrap = Bootstrap()
celery = Celery()


# babel = Babel()


class MyModelView(sqla.ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login', next=request.url))


admin = Admin(index_view=AdminIndexView(), template_mode='bootstrap4')


class MyAdminIndexView(AdminIndexView):

    @expose('/')
    @has_role('admin')
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.register'))
        return super(MyAdminIndexView, self).index()


def create_app(config_class=Config):
    """
    An flask application factory, as explained here:
    http://flask.pocoo.org/docs/patterns/appfactories/
    env ( set/export CONFIG_TYPE)
    Arguments:
        object_name: the python path of the config object,
                     e.g. project.config.ProdConfig
    """
    app = Flask(__name__)
    #CONFIG_TYPE = os.getenv('CONFIG_TYPE', default='config.ProdConfig')
    app.config.from_object(config_class)

    # UPLOAD_FOLDER = 'static/img/'
    # app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    fa.init_app(app)
    bootstrap.init_app(app)
    celery.init_app(app)

    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask

    # babel.init_app(app)
    app.static_folder = 'static'

    admin.init_app(app)
    from .auth.models import User, Referrer, Role, Transactions, Investments
    admin.add_view(MyModelView(User, db.session))
    admin.add_view(MyModelView(Referrer, db.session))
    admin.add_view(MyModelView(Role, db.session))
    admin.add_view(MyModelView(Transactions, db.session))
    admin.add_view(MyModelView(Investments, db.session))

    from .auth import create_module as auth_create_module
    from .earncoins import create_module as earncoins_create_module
    from .main import create_module as main_create_module

    auth_create_module(app)
    earncoins_create_module(app)
    main_create_module(app)

    return app


