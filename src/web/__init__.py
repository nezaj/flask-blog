import os
import logging

from flask import Flask
from config import app_config
from loghandlers import get_stderr_handler, configure_sqlalchemy_logger
from web import assets
from data.db import DatabaseConnection

class BlogApp(Flask):

    db = None  # initialized later

    def __init__(self, config_obj):
        super(BlogApp, self).__init__(__name__)
        self.config.from_object(config_obj)

def configure_loggers(app):
    " Sets up app and sqlalchemy loggers "

    # Set up app.logger to emit messages according to configuration
    app.logger.setLevel(level=app.config["APP_LOG_LEVEL"])
    stderr_handler = get_stderr_handler(
        app.config["STDERR_LOG_FORMAT"],
        level=app.config["APP_LOG_LEVEL"])

    # Flask enables a handler that writes to stderr by default in debug mode
    if not app.debug:
        app.logger.addHandler(stderr_handler)

    configure_sqlalchemy_logger(
        app.config["STDERR_LOG_FORMAT"],
        level=app.config["SQLALCHEMY_LOG_LEVEL"])

def initialize_db(app):
    db_url = app.config['SQLALCHEMY_DATABASE_URI']
    app.db = DatabaseConnection(db_url)
    app.logger.info("Connected to {}".format(repr(app.db.engine.url)))

    @app.teardown_appcontext
    def remove_session(response):  # pylint: disable=W0612
        app.db.session.remove()
        return response

def initialize_app(app):
    " Do any one-time initialization of the app prior to serving "
    app.static_folder = app.config['STATIC_DIR']
    initialize_db(app)
    assets.register_assets(app)

def create_app():
    " Factory for creating app "
    app = BlogApp(app_config)
    configure_loggers(app)
    initialize_app(app)

    return app

app = create_app()

# Import routes and template filters
from web import views
from web import templating
