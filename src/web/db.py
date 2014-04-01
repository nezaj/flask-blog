from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Query, scoped_session
from sqlalchemy.schema import MetaData
from sqlalchemy.ext.declarative import declarative_base

class DatabaseConnection(object):
    " A database connection "

    def __init__(self, url, **factory_args):
        self.engine = create_engine(url)
        self.session_factory = sessionmaker(bind=self.engine, query_cls=Query, **factory_args)
        self.session = scoped_session(self.session_factory)

def named_declarative_base():
    """
    Returns a declarative base SQLAlchemy object with naming conventions
    for indexes, unique-keys, constraints, foreign-keys, and primary-keys.

    This is useful for altering tables. See below for details
    http://docs.sqlalchemy.org/en/rel_0_9/core/constraints.html#constraint-naming-conventions
    """
    convention = {
        "ix": 'ix_%(column_0_label)s',
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    }
    metadata = MetaData(naming_convention=convention)

    return declarative_base(metadata=metadata)
