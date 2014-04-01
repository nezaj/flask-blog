"""
Defines config settings based on 'FLASK_BLOG_ENV' enviornment variable.
Defaults to development configuration if 'FLASK_BLOG_ENV' is not set

app_config is used throughout the project to access config settings
for creating the app, using alembic, generating posts, etc.
"""

import os
from settings import DevConfig, HerokuConfig, TestConfig

# Config settings
config_dict = {
    'dev': DevConfig,
    'heroku': HerokuConfig,
    'test': TestConfig
}

app_env = os.getenv('FLASK_BLOG_ENV')
app_config = config_dict.get(app_env) or DevConfig
