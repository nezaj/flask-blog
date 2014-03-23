from sqlalchemy import func
from web import db

tags = db.Table('tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'))
)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.Integer)
    title = db.Column(db.String(120), unique=True)
    slug = db.Column(db.String(120), index=True, unique=True)
    content = db.Column(db.Text)

    published_dt = db.Column(db.DateTime, default=None)
    published = published_dt != None

    tags = db.relationship('Tag', secondary="tags", backref=db.backref("posts", lazy="dynamic"))

    def __init__(self, author, title, slug, content, published_dt):
        self.author = author
        self.title = title
        self.slug = slug
        self.content = content
        self.published_dt = published_dt

    def __repr__(self):
        return '<Post {}>'.format(self.title)

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), index=True, unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Tag {}>'.format(self.name)
