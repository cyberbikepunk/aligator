""" This module instantiates a Flask application. """

from flask import Flask
from config import choose
from .blog.views import blog
from flask.ext.bootstrap import Bootstrap
from os import getenv
from flask.ext.script import Manager
from flask import redirect


def create_app(environment_name):
    app_ = Flask(__name__)

    environment = choose[environment_name]
    app_.config.from_object(environment)
    environment.init_app(app_)

    app_.register_blueprint(blog)

    return app_


enviroment_name = getenv('ALIGATOR_ENVIRONMENT', 'production')
app = create_app(enviroment_name)

bootstrap = Bootstrap(app)
manager = Manager(app)


@app.route('/')
def index():
    return redirect('/blog/')

