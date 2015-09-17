""" Global configuration settings. """


from os.path import dirname, join, abspath
base_dir = abspath(dirname(__file__))


class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + join(base_dir, 'production.db')

    def init_app(self):
        pass


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + join(base_dir, 'development.db')
    DEBUG = True


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + join(base_dir, 'testing.db')
    TESTING = True


class ProductionConfig(Config):
    pass

