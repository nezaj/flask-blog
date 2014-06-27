from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String

from .base import Base

class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    name = Column(String(40), index=True, unique=True)

    def __repr__(self):
        return '<Tag {}>'.format(self.name)
