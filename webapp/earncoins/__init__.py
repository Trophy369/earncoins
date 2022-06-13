def create_module(app, **kwargs):

    from .views import earncoins_blueprint
    app.register_blueprint(earncoins_blueprint)
