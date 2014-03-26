#!/usr/bin/env python

" Script to re-create the database "

import config
from web.db import DatabaseConnection
from web.models import Base
from manage_posts import publish_post, generate_post

def prepopulate_db():

    class Post(object):

        @classmethod
        def new(self, title):
            return Post('nezaj', title)

        def __init__(self, author, title):
            self.author = author
            self.title = title

    sample_posts = ["Hello World", "Meaning of Life", "The Universe"]
    for post in sample_posts:
        p = Post.new(post)
        generate_post(p, force=True)
        publish_post(p, force=True)

def stamp_db():
    """
    Creates alembic_version table if it doesn't already exist
    and stamps it with the head revision
    """

    import os
    from alembic.config import Config
    from alembic import command

    current_dir = os.path.dirname(os.path.abspath(__file__))
    alembic_ini_path = os.path.join(current_dir, 'alembic.ini')
    alembic_cfg = Config(alembic_ini_path)

    command.stamp(alembic_cfg, "head")

def rebuild_db():
    " Recreates the db and stamps it with the latest revision "

    db_url = config.config_obj.SQLALCHEMY_DATABASE_URI
    db = DatabaseConnection(db_url)

    Base.metadata.drop_all(db.engine)
    Base.metadata.create_all(db.engine)
    stamp_db()

if __name__ == '__main__':
    rebuild_db()
    prepopulate_db()
    print 'database rebuilt!'
