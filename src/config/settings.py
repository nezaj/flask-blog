"""
Configures app settings for dev, testing, and Heroku
"""

import os
import logging

from sqlalchemy.engine.url import URL

class BaseConfig(object):
    # controls whether web interfance users are in Flask debug mode
    # (e.g. Werkzeug stack trace console, unminified assets)
    DEBUG = False

    # Loggging
    APP_LOG_LEVEL = logging.DEBUG
    SQLALCHEMY_LOG_LEVEL = logging.WARN
    STDERR_LOG_FORMAT = ('%(asctime)s %(levelname)s %(message)s','%m/%d/%Y %I:%M:%S %p')

    # Location of db connection. Use in-memory db by default
    SQLALCHEMY_DATABASE_URI = URL(drivername='sqlite', database=None)

    # Useful directories
    CONFIG_DIR = os.path.dirname(os.path.abspath(__file__))
    SRC_DIR = os.path.dirname(CONFIG_DIR)
    POSTS_DIR = os.path.join(SRC_DIR, 'posts')
    TEST_DIR = os.path.join(SRC_DIR, 'test')
    WEB_DIR = os.path.join(SRC_DIR, 'web')
    STATIC_DIR = os.path.join(WEB_DIR, 'static')

    # Location of alembic config file
    ALEMBIC_INI_PATH = os.path.join(SRC_DIR, 'alembic.ini')

class DevConfig(BaseConfig):
    ENV = 'dev'

    # Enable the flask debugger
    DEBUG = True

    # DB is located in web directory
    db_path = os.path.join(BaseConfig.WEB_DIR, 'dev.db')
    SQLALCHEMY_DATABASE_URI = URL(drivername='sqlite', database=db_path)

class TestConfig(BaseConfig):
    ENV = 'test'
    POSTS_DIR = os.path.join(BaseConfig.TEST_DIR, 'posts')

    # Don't want to see info messages about managing posts
    APP_LOG_LEVEL = logging.WARN

    # DB is located in test directory
    db_path = os.path.join(BaseConfig.TEST_DIR, 'dev.db')
    SQLALCHEMY_DATABASE_URI = URL(drivername='sqlite', database=db_path)

class HerokuConfig(BaseConfig):
    ENV = 'prod'

    # Don't need to see debug messages in production
    APP_LOG_LEVEL = logging.INFO

    # This must be defined in Heroku
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
