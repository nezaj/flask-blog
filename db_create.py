#!/usr/bin/env python

" Script to re-create the database "

from web import db
from publish import publish_post
from generate import generate_post


class Post(object):

    @classmethod
    def new(self, title):
        return Post('nezaj', title)

    def __init__(self, author, title):
        self.author = author
        self.title = title

def prepopulate():
    sample_posts = ["Hello World", "Meaning of Life", "The Universe"]
    for post in sample_posts:
        p = Post.new(post)
        generate_post(p)
        publish_post(p)

if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    prepopulate()
    print 'database rebuilt!'
