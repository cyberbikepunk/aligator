""" The flask application manager lauches the application. """

from flask.ext.bootstrap import Bootstrap
from app import create_app
from os import getenv
from flask.ext.script import Manager


enviroment_name = getenv('ALIGATOR_ENVIRONMENT', 'production')
app = create_app(enviroment_name)

bootstrap = Bootstrap(app)
manager = Manager(app)

if __name__ == '__main__':
    manager.run()
