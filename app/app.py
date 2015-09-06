from flask import Flask, render_template
from celery import Celery

from .config import BaseConfig, DefaultConfig
from .extensions import db, login_manager


__all__ = ['create_app']


def create_app(config=None, app_name=None, register_blueprints=True):
    """
    Create Flask app
    """

    if app_name is None:
        app_name = BaseConfig.PROJECT_NAME

    app = Flask(app_name)
    configure_app(app, config)

    # So no circular import when using Celery
    if register_blueprints:
        configure_blueprints(app)

    configure_extensions(app)
    configure_error_handlers(app)

    return app


def create_celery(app=None):
    celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery


def configure_app(app, config=None):
    """
    Read config from object
    """

    app.config.from_object(DefaultConfig)

    if config:
        app.config.from_object(config)


def configure_blueprints(app):
    """
    Register blueprints
    """

    # Break the circular import
    from .module_one import module_one

    blueprints = {
        '': module_one
    }

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
    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("page_not_found.html"), 404
