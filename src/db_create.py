#!/usr/bin/env python

" Script to re-create the database and populate it with some sample posts"

from config import app_config
from web.db import DatabaseConnection
from web.models import Base
from manage import publish_post, generate_post
from test.generate_tools import generate_post as dummy_post

def prepopulate_db():

    sample_titles = ["Hello World", "Meaning of Life", "The Universe"]
    for title in sample_titles:
        p = dummy_post("nezaj", title)
        generate_post(p, force=True)
        publish_post(p, force=True)

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
    stamp_db()

if __name__ == '__main__':
    rebuild_db()
    prepopulate_db()
    print 'database rebuilt!'
