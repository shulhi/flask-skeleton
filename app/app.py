from flask import Flask, render_template

from .config import BaseConfig, DefaultConfig
from .extension import db, login_manager

from .module_one import module_one


__all__ = ['create_app']


DEFAULT_BLUEPRINTS = {
    '/one': module_one
}


def create_app(config=None, app_name=None, blueprints=None):
    """
    Create Flask app
    """

    if app_name is None:
        app_name = BaseConfig.PROJECT_NAME
    if blueprints is None:
        blueprints = DEFAULT_BLUEPRINTS

    app = Flask(app_name)
    configure_app(app, config)
    configure_blueprints(app, blueprints)
    configure_extensions(app)
    configure_error_handlers(app)

    return app


def configure_app(app, config=None):
    """
    Read config from object
    """

    app.config.from_object(DefaultConfig)

    if config:
        app.config.from_object(config)


def configure_blueprints(app, blueprints):
    """
    Register blueprints
    """

    for url, blueprint in blueprints.iteritems():
        app.register_blueprint(blueprint, url_prefix=url)


def configure_extensions(app):
    """
    Configure third party extensions
    """

    # Flask SQLAlchemy
    db.init_app(app)

    # Flask login
    @login_manager.user_loader
    def load_user(id):
        # Should return with given id
        # i.e. return User.query.get(id)
        pass

    login_manager.init_app(app)


def configure_error_handlers(app):
    @app.errohandler(404):
    def page_not_found(error):
        return render_template("page_not_found.html"), 404
