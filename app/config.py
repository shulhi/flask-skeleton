import os

class BaseConfig(object):
    """
    Base configuration
    """

    # Project name must be based on parent dir (app or whatever user defined)
    # so that when running render_template, etc, it will pass the correct path to Flask
    # i.e current dir is app, thus project name is 'app'
    # if PROJECT_NAME is set manually, ensure dir name is changed to the same name
    PROJECT_NAME = os.path.split(os.path.dirname(os.path.realpath(__file__)))[1]

    SECRET_KEY = 'WHATWHATINTHEBUTT'


class DefaultConfig(BaseConfig):
    DEBUG = True

    SQLALCHEMY_ECHO = False
    SQLALCHEMY_DATABASE_URI = "postgresql://username:password@host/database"

    CELERY_BROKER_URL = 'amqp://127.0.0.1'
    CELERY_RESULT_BACKEND = 'rpc'
    CELERY_TRACK_STARTED = True


class TestConfig(BaseConfig):
    TESTING = True

    # Disable WTForm CSRF protection
    WTF_CSRF_ENABLED = False

    SQLALCHEMY_ECHO = False
    SQLALCHEMY_DATABASE_URI = "postgresql://username:password@host/database"
