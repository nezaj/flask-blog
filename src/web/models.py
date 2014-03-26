from sqlalchemy import func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.schema import Column, ForeignKey, Table
from sqlalchemy.types import Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base

from web.db import named_declarative_base

Base = named_declarative_base()

tags = Table('post_tags', Base.metadata,
    Column('tag_id', Integer, ForeignKey('tags.id')),
    Column('post_id', Integer, ForeignKey('posts.id'))
)

class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    author = Column(Integer)
    title = Column(String(120), unique=True)
    slug = Column(String(120), index=True, unique=True)
    content = Column(Text)

    published_dt = Column(DateTime, default=None)
    published = published_dt != None

    tags = relationship('Tag', secondary="post_tags", backref=backref("posts", lazy="dynamic"))

    def __init__(self, author, title, slug, content, published_dt):
        self.author = author
        self.title = title
        self.slug = slug
        self.content = content
        self.published_dt = published_dt

    def __repr__(self):
        return '<Post {}>'.format(self.title)

class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    name = Column(String(40), index=True, unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Tag {}>'.format(self.name)
