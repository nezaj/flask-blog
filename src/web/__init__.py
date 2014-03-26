import os
from flask import Flask

import config
from web import assets
from web import db

web_directory = os.path.abspath(os.path.dirname(__file__))

class BlogApp(Flask):

    db = None # initialized later

    def __init__(self, config_obj):
        super(BlogApp, self).__init__(__name__)
        self.config.from_object(config_obj)

def initialize_db(app):
    db_url = app.config['SQLALCHEMY_DATABASE_URI']
    app.db = db.DatabaseConnection(db_url)

    @app.teardown_appcontext
    def remove_session(response):
        app.db.session.remove()
        return response

def initialize_app(app):
    initialize_db(app)
    assets.register_assets(app)

def create_app():
    " Makes the Flask app. "
    config_obj = config.config_obj
    app = BlogApp(config_obj)
    initialize_app(app)

    return app

app = create_app()

# Import routes and template filters
from web import views
from web import templating
