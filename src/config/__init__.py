"""
Imports config settings based on 'FLASK_BLOG_ENV' enviornment variable.
Defaults to development configuration if 'FLASK_BLOG_ENV' is not set
"""

import os
from settings import DevConfig, HerokuConfig, TestConfig

config_dict = {
    'dev': DevConfig,
    'heroku': HerokuConfig,
    'test': TestConfig
}

config_env = os.getenv('FLASK_BLOG_ENV')
config_obj = config_dict.get(config_env) or DevConfig


