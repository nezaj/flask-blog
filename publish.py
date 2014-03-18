#!/usr/bin/env python
import argparse
import os

from web import db
from web.models import Post

static_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'web/static/posts')


def publish_post(args):
    file_name = args.title.replace(' ', '_').lower() + ".txt"
    file_path = os.path.join(static_directory, file_name)

    with open(file_path, 'r') as f:
        author = f.readline().strip('n')
        title = f.readline().strip('\n')
        _ = f.readline() # throw-away one line
        content = f.read()

    author = author[author.find(':') + 2:]
    title = title[title.find(':') + 2:]
    p = Post.query.filter_by(title=title).first()

    if p:
        resp = raw_input("{} already exists! Do you want to over_write (y/n)? ".format(title))
        if resp != 'y':
            print "{} was not added to the db".format(title)
            return
        else:
            db.session.delete(p)
            db.session.commit()

    new_post = Post(author=author, title=title, content=content)
    db.session.add(new_post)
    db.session.commit()
    print "Added {} to the db!".format(title)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Tool for publishing posts")
    parser.set_defaults(func=publish_post)

    parser.add_argument('title', type=clean_title, help="Title of post")

    args = parser.parse_args()
    args.func(args)
