import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.assets import Environment, Bundle

from config import config_obj

web_directory = os.path.abspath(os.path.dirname(__file__))

class BlogApp(Flask):

    db = None # initialized later

    def __init__(self, config_obj):
        super(BlogApp, self).__init__(__name__)
        self.config.from_object(config_obj)

def register_assets(app):
    assets = Environment(app)
    assets.url = app.static_url_path

    CSS_ASSETS = [
        'css/vendor/readable-bootstrap.css',
        'css/vendor/font-awesome.css',
        Bundle('css/application.scss', filters='pyscss', output='css/compiled-scss.css')
    ]

    css = Bundle(*CSS_ASSETS, filters='cssmin', output='css/bundle.min.css')
    assets.register('scss_all', css)
    return assets

app = BlogApp(config_obj)
register_assets(app)
app.db = SQLAlchemy(app)

from web import views, models, templating
