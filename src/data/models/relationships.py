from sqlalchemy.schema import Column, ForeignKey, Table
from sqlalchemy.types import Integer

from .base import Base

post_tags = Table(
    'post_tags', Base.metadata,
    Column('tag_id', Integer, ForeignKey('tags.id')),
    Column('post_id', Integer, ForeignKey('posts.id'))
)
