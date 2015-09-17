""" This module instantiates a Flask application. """

from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy

from .blog.views import main


bootstrap = Bootstrap()
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.debug = True
    app.register_blueprint(main)

    bootstrap.init_app(app)
    db.init_app(app)

    return app
