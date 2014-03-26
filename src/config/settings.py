import os
from sqlalchemy.engine.url import URL

# TODO: UGLY
web_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'web'))

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

class DevConfig(BaseConfig):
    DEBUG = True
    RELOAD = True
    db_path = os.path.join(web_directory, 'dev.db')
    SQLALCHEMY_DATABASE_URI = URL(drivername='sqlite', database=db_path)

class HerokuConfig(BaseConfig):
    # TODO: Make this point to the right thing
    db_path = os.path.join(web_directory, 'dev.db')
    SQLALCHEMY_DATABASE_URI = URL(drivername='sqlite', database=db_path)
    # SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

class TestConfig(BaseConfig):
    TESTING = True
