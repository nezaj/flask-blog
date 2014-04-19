from sqlalchemy.orm import relationship, backref
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String, Text, DateTime
from sqlalchemy.ext.hybrid import hybrid_property

from .base import Base
from .relationships import post_tags

class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    author = Column(String(60))
    title = Column(String(120), unique=True)
    slug = Column(String(120), index=True, unique=True)
    content = Column(Text)

    published_dt = Column(DateTime, index=True, default=None)
    @hybrid_property
    def published(self):
        return self.published_dt != None

    tags = relationship('Tag', secondary=post_tags, backref=backref("posts", lazy="dynamic"))

    def __repr__(self):
        return '<Post {}>'.format(self.title)
