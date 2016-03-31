""" Global configuration settings. """


class BaseConfig:
    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(BaseConfig):
    ENVIRONMENT = 'development'
    DEBUG = True


class TestingConfig(BaseConfig):
    ENVIRONMENT = 'testing'
    TESTING = True


class ProductionConfig(BaseConfig):
    ENVIRONMENT = 'production'


choose = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}
