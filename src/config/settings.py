"""
Configures app settings for dev, testing, and Heroku
"""

import os
from sqlalchemy.engine.url import URL

class BaseConfig(object):
    # controls whether web interfance users are in Flask debug mode
    # (e.g. Werkzeug stack trace console, unminified assets)
    DEBUG = False

    # Controls Flask testing mode (controls some error handling)
    TESTING = False

    # Controls whether we reload things from the filesystem if they change
    # (e.g. Werkzeug reloader, templates, assets): Makes sense only for dev
    RELOAD = False

    # Location of db connection. Use in-memory db by default
    SQLALCHEMY_DATABASE_URI = URL(drivername='sqlite', database=None)

    # Useful directories
    CONFIG_DIR = os.path.dirname(os.path.abspath(__file__))
    SRC_DIR = os.path.dirname(CONFIG_DIR)
    WEB_DIR = os.path.join(SRC_DIR, 'web')
    STATIC_DIR = os.path.join(WEB_DIR, 'static')
    POSTS_DIR = os.path.join(STATIC_DIR, 'posts')

    # Location of alembic config file
    ALEMBIC_INI_PATH = os.path.join(SRC_DIR, 'alembic.ini')

class DevConfig(BaseConfig):
    DEBUG = True
    RELOAD = True
    db_path = os.path.join(BaseConfig.WEB_DIR, 'dev.db')
    SQLALCHEMY_DATABASE_URI = URL(drivername='sqlite', database=db_path)

class TestConfig(BaseConfig):
    TESTING = True

class HerokuConfig(BaseConfig):
    # TODO: Make this point to the right thing
    db_path = os.path.join(BaseConfig.WEB_DIR, 'dev.db')
    SQLALCHEMY_DATABASE_URI = URL(drivername='sqlite', database=db_path)
    # SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
