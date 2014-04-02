from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Query, scoped_session

from config import app_config

class DatabaseConnection(object):
    " A database connection "

    def __init__(self, url, **factory_args):
        self.engine = create_engine(url)
        self.session_factory = sessionmaker(bind=self.engine, query_cls=Query, **factory_args)
        self.session = scoped_session(self.session_factory)

def get_db():
    " Returns a database connection based on current config "
    db_url = app_config.SQLALCHEMY_DATABASE_URI
    return DatabaseConnection(db_url)
