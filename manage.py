""" The flask application manager lauches the application. """

from flask.ext.bootstrap import Bootstrap
from flask.ext.mail import Mail
from flask.ext.moment import Moment
from flask.ext.sqlalchemy import SQLAlchemy
from app import create_app
from os import getenv
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand


enviroment_name = getenv('ALIGATOR_ENVIRONMENT', 'production')
app = create_app(enviroment_name)

bootstrap = Bootstrap(app)
mail = Mail(app)
moment = Moment(app)
manager = Manager(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
