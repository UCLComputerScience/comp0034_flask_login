"""Flask config class."""
from os.path import dirname, abspath, join


class Config(object):
    """Set Flask base configuration"""
    CSRF_ENABLED = True
    SECRET_KEY = 'dfdQbTOExternjy5xmCNaB'
    ENV = 'development'

    # Database config
    CWD = dirname(abspath(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + join(CWD, 'simpsons.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProdConfig(Config):
    # ENV = 'production' sets TESTING to False, DEBUG to False
    ENV = 'production'


class TestConfig(Config):
    # ENV = 'testing' sets TESTING to True, DEBUG to False
    ENV = 'testing'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


class DevConfig(Config):
    # ENV = 'development' sets TESTING to False, DEBUG to True
    ENV = 'development'
    TESTING = False
    DEBUG = True


config = {
    'DevConfig': DevConfig,
    'TestConfig': TestConfig,
    'ProdConfig': ProdConfig
}
