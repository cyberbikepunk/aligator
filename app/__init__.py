""" This module instantiates a Flask application. """

from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.mail import Mail
from flask.ext.moment import Moment
from config import choose
from .blog.views import blog


bootstrap = Bootstrap()
db = SQLAlchemy()
mail = Mail()
moment = Moment()


def create_app(environment_name):
    app = Flask(__name__)

    environment = choose[environment_name]
    app.config.from_object(environment)

    app.register_blueprint(blog)

    environment.init_app(app)
    moment.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    db.init_app(app)

    return app
