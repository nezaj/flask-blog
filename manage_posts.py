#!/usr/bin/env python

" Script to manage blog posts "

import argparse
import os

from sqlalchemy import func
from web import db
from web.models import Post
from util import posts_directory, clean_title, get_post_path, overwrite_file, slugify


def delete_post(args):
    " Deletes a file at the specified file-path "
    # TODO: Make this delete the post in the db as well
    post_path = get_post_path(args.title)

    if os.path.isfile(post_path):
        os.remove(post_path)
        print "Removed {}".format(post_path)
    else:
        print "Error: Could not find {}".format(post_path)

def publish_post(args, force=False):
    post_path = get_post_path(args.title)

    # Open the file and read contents
    try:
        with open(post_path, 'r') as f:
            author = f.readline().strip('n')
            title = f.readline().strip('\n')
            _ = f.readline() # throw-away line
            content = f.read()
    except IOError:
        print "Error: Could not find {}".format(post_path)
        return

    # Process post attributes
    author = author[author.find(':') + 2:]
    title = title[title.find(':') + 2:]
    slug = slugify(title)

    # Prompt whether to remove post if already exists in db
    p = Post.query.filter_by(title=title).first()
    if not force and p:
        resp = raw_input("Post with title '{}' already exists! Do you want to overwite (y/n)? ".format(title))
        if resp != 'y':
            print "'{}' was not added to the db".format(title)
            return
        else:
            db.session.delete(p)
            db.session.commit()

    # Add new post to db
    new_post = Post(
        author=author,
        title=title,
        slug=slug,
        content=content,
        published_dt=func.now()
        )
    db.session.add(new_post)
    db.session.commit()
    print "Added {} to the db!".format(title)

def generate_post(args, force=False):
    """
    Generates a new file with a skeleton for the blog post and
    saves it into the static posts directory.

    The file name is the slug.txt. If the file already exists
    user is prompted whether to overwrite the file.
    """

    post_path = get_post_path(args.title)

    # Check to see if file exists, if it does prompt for overwite
    if not force and os.path.isfile(post_path):
        if not overwrite_file(post_path):
            print "{} was not re-generated".format(post_path)
            return

    # Create post skeleton
    with open(post_path, 'w') as f:
        f.write("Author: {}\n".format(args.author))
        f.write("Title: {}\n".format(args.title))
        f.write("\n") # Extra newline at the end

    print "Generated new file at {}".format(post_path)

def list_posts(args):
    " List published and unpublished posts "
    # TODO: This is kind of useless right now. Make it better

    def display_posts(posts):
        for p in posts:
            print p.title

    published_posts = db.session.query(Post).filter(Post.published).order_by(Post.published_dt.desc()).all()
    unpublished_posts = db.session.query(Post).filter(~Post.published).all()

    print 'Published Posts:\n'
    print display_posts(published_posts) if published_posts else "You haven't published anything. Get to publishing!"

    print 'Unpublished Posts:\n'
    print display_posts(unpublished_posts) if unpublished_posts else "You've published everything. Maybe write some more?"

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Tools for managing posts")
    subparsers = parser.add_subparsers()

    # Parser for publishing static files
    list_parser = subparsers.add_parser('list',
    description="List published and unpublished files")
    list_parser.set_defaults(func=list_posts)

    # Parser for publishing static files
    publish_parser = subparsers.add_parser('publish',
    description="Publish static file")
    publish_parser.set_defaults(func=publish_post)
    publish_parser.add_argument('title', type=clean_title, help="Title of post")

    # Parser for generating static files
    generate_parser = subparsers.add_parser('generate',
    description="Generate static file")
    generate_parser.set_defaults(func=generate_post)
    generate_parser.add_argument('title', type=clean_title, help="Title of post")
    generate_parser.add_argument("-a", "--author", default="nezaj", help="Author of post")

    # Parser for deleting static files
    delete_parser = subparsers.add_parser('delete',
    description="Delete static file")
    delete_parser.set_defaults(func=delete_post)
    delete_parser.add_argument('title', type=clean_title, help="Title of post")

    args = parser.parse_args()
    args.func(args)
