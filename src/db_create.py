#!/usr/bin/env python

"""
Script to re-create the database and populate it with some sample posts
"""

from config import app_config
from data.db import DatabaseConnection
from data.models import Base
from commands import publish_post, generate_post
from test.generate_tools import generate_post as dummy_post
from loggers import get_stderr_logger

def prepopulate_db():

    logger = get_stderr_logger()

    for _ in xrange(0, 50):
        p = dummy_post()
        generate_post(p, logger, force=True)
        publish_post(p, logger)

def stamp_db():
    """
    Creates alembic_version table if it doesn't already exist
    and stamps it with the head revision
    """
    from alembic.config import Config
    from alembic import command

    alembic_cfg = Config(app_config.ALEMBIC_INI_PATH)
    command.stamp(alembic_cfg, "head")

def rebuild_db():
    " Recreates the db and stamps it with the latest revision "
    db_url = app_config.SQLALCHEMY_DATABASE_URI
    db = DatabaseConnection(db_url)

    Base.metadata.drop_all(db.engine)
    Base.metadata.create_all(db.engine)

if __name__ == '__main__':
    rebuild_db()

    if not app_config.ENV == 'prod':
        stamp_db()
        prepopulate_db()

    print 'database rebuilt!'
