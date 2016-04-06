""" This module instantiates the Alligator application. """


from os import getenv
from flask import Flask
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask import redirect

from app.blog.views import blog
from config import choose


def create_app():
    app_ = Flask(__name__)

    environment = getenv('ALLIGATOR_ENVIRONMENT', 'production')
    configuration = choose[environment]
    app_.config.from_object(configuration)
    configuration.init_app(app_)
    app_.register_blueprint(blog)

    return app_


app = create_app()
bootstrap = Bootstrap(app)
manager = Manager(app)


@app.route('/')
def index():
    return redirect('/blog/')
