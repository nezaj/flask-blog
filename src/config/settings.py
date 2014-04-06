"""
Configures app settings for dev, testing, and Heroku
"""

import os
from sqlalchemy.engine.url import URL

class BaseConfig(object):
    # controls whether web interfance users are in Flask debug mode
    # (e.g. Werkzeug stack trace console, unminified assets)
    DEBUG = False

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
    DEBUG = True
    db_path = os.path.join(BaseConfig.WEB_DIR, 'dev.db')
    SQLALCHEMY_DATABASE_URI = URL(drivername='sqlite', database=db_path)

class TestConfig(BaseConfig):
    POSTS_DIR = os.path.join(BaseConfig.TEST_DIR, 'posts')
    db_path = os.path.join(BaseConfig.TEST_DIR, 'dev.db')
    SQLALCHEMY_DATABASE_URI = URL(drivername='sqlite', database=db_path)

class ProdConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
