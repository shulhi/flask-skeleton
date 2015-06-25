from flask.ext.testing import TestCase

from app.config import TestConfig
from app.extensions import db


class BaseCase(TestCase):
    """
    This is the base case for test.
    Ideally, you should inherit your test classes from this class.
    """

    def create_app(self):
        app = create_app(config=TestConfig)
        return app


    def init_seed(self):
        """
        Init seed data for database
        """
        pass


    def setUp(self):
        db.create_all()
        self.init_seed()


    def tearDown(self):
        db.session_remove()
        db.drop_all()
