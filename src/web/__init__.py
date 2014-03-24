import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.assets import Environment, Bundle

web_directory = os.path.abspath(os.path.dirname(__file__))

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

app = Flask(__name__)
register_assets(app)

### TODO: Hacky, come up with a better way
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:////tmp/test.db')

db = SQLAlchemy(app)

from web import views, models, templating
