from sqlalchemy.orm import relationship, backref
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String, Text, DateTime

from .base import Base
from .relationships import post_tags

class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    author = Column(Integer)
    title = Column(String(120), unique=True)
    slug = Column(String(120), index=True, unique=True)
    content = Column(Text)

    published_dt = Column(DateTime, index=True, default=None)
    published = published_dt != None

    tags = relationship('Tag', secondary=post_tags, backref=backref("posts", lazy="dynamic"))

    def __repr__(self):
        return '<Post {}>'.format(self.title)
