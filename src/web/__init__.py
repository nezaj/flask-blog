import os
from flask import Flask

import config
from web import assets, db

class BlogApp(Flask):

    db = None # initialized later

    def __init__(self, app_config):
        super(BlogApp, self).__init__(__name__)
        self.config.from_object(app_config)

def initialize_db(app):
    db_url = app.config['SQLALCHEMY_DATABASE_URI']
    app.db = db.DatabaseConnection(db_url)

    @app.teardown_appcontext
    def remove_session(response):
        app.db.session.remove()
        return response

def initialize_app(app):
    app.static_folder = app.config['STATIC_DIR']
    initialize_db(app)
    assets.register_assets(app)

def create_app():
    " Makes the Flask app. "
    app_config = config.app_config
    app = BlogApp(app_config)
    initialize_app(app)

    return app

app = create_app()

# Import routes and template filters
from web import views
from web import templating
