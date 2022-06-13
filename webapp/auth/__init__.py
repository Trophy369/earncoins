from flask_login import LoginManager

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.session_protection = "basic"
login_manager.login_message = "Please login to access this page"
login_manager.login_message_category = "info"


def create_module(app, **kwargs):
    login_manager.init_app(app)
    from .views import auth_blueprint
    app.register_blueprint(auth_blueprint)
