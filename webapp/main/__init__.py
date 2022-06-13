from .views import main_blueprint
#from ..auth.models import Permission


def create_module(app, **kwargs):
    app.register_blueprint(main_blueprint)


# @main_blueprint.app_context_processor
# def inject_permissions():
#     return dict(Permission=Permission)



