#!/usr/bin/env python

from flask.ext.script import Manager

from app import create_app
from app.extensions import db


app = create_app()
manager = Manager(app)


@manager.command
def run():
    app.run()


@manager.command
def initdb():
    db.drop_all()
    db.create_all()


if __name__ == "__main__":
    manager.run()
