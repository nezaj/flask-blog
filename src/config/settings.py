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

class DevConfig(BaseConfig):
    DEBUG = True
    RELOAD = True
    SQLALCHEMY_DATABASE_URI = URL(drivername='sqlite', database='dev.db')

class HerokuConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = URL(drivername='sqlite', database='dev.db')
    # SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

class TestConfig(BaseConfig):
    TESTING = True

from settings import DevConfig, HerokuConfig, TestConfig
config_dict = {
    'dev': DevConfig,
    'heroku': HerokuConfig,
    'test': TestConfig
}


