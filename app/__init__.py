""" This module instantiates a Flask application. """

from flask import Flask
from config import choose
from .blog.views import blog


def create_app(environment_name):
    app = Flask(__name__)

    environment = choose[environment_name]
    app.config.from_object(environment)
    environment.init_app(app)

    app.register_blueprint(blog)

    return app
