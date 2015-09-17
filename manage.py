""" The flask application manager lauches the application. """


from app import create_app
from os import getenv


enviroment_name = getenv('ALIGATOR_ENVIRONMENT', 'production')
app = create_app(enviroment_name)


if __name__ == '__main__':
    app.run()
