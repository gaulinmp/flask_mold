# -*- coding: utf-8 -*-
import os

os_env = os.environ


class Config(object):
    SITE_NAME = "Test App"
    SITE_AUTHOR = "Mac Gaulin"
    SITE_DESCRIPTION = "Test flask site."
    GOOGLE_ANALYTICS = ''
    SECRET_KEY = os_env.get('LOGGING_SERVER_SECRET',
                            'fan;iofasn;oifaxn;axeoihsena;903wyanwop3thjnlej')
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # config directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    SESSION_LOG_FILENAME = 'login.dat'
    SESSION_LOG_FILE_PATH = os.path.join(APP_DIR, SESSION_LOG_FILENAME)
    BCRYPT_LOG_ROUNDS = 13
    WTF_CSRF_ENABLED = True
    USE_CDN = True


class ProdConfig(Config):
    """Production configuration."""
    ENV = 'prod'
    DEBUG = False


class DevConfig(Config):
    """Development configuration."""
    ENV = 'dev'
    DEBUG = True
    DB_NAME = 'dev.db'
    SQLALCHEMY_DATABASE_URI = ('sqlite:///' +
                                os.path.join(Config.PROJECT_ROOT, DB_NAME))
    USE_CDN = False


class TestConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    BCRYPT_LOG_ROUNDS = 1  # For faster tests
    WTF_CSRF_ENABLED = False  # Allows form testing
    USE_CDN = False
