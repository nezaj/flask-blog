from sqlalchemy import func
from web import db

tags = db.Table('tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'))
)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.Integer)
    title = db.Column(db.String(120), index=True, unique=True)
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, nullable=False, default=func.now())

    tags = db.relationship('Tag', secondary="tags", lazy='dynamic', backref=db.backref("posts", lazy="dynamic"))

    def __init__(self, author, title, content):
        self.author = author
        self.title = title
        self.content = content

    def __repr__(self):
        return '<Post {}>'.format(self.title)

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), index=True, unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Tag {}>'.format(self.name)
