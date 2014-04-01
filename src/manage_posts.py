#!/usr/bin/env python

"""
Parsers for managing posts. Currently supported commands are:
Usage: ./manage_posts <command> <args>

- generate <args>: Creates a new static file in folder directory
- publish <args>: Adds a static file to the db
- list: Lists published/unpublished posts
- delete <args>: Deletes specified file from static folder and db
"""

import argparse
from manage import generate_post, publish_post, list_posts, delete_post
from util import clean_title

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Tools for managing posts")
    subparsers = parser.add_subparsers()

    # Parser for listing published and unpublished files
    list_parser = subparsers.add_parser('list',
    description="List published and unpublished files")
    list_parser.set_defaults(func=list_posts)

    # Parser for adding static files to db
    publish_parser = subparsers.add_parser('publish',
    description="Publish static file")
    publish_parser.set_defaults(func=publish_post)
    publish_parser.add_argument('title', type=clean_title, help="Title of post")

    # Parser for generating static files
    generate_parser = subparsers.add_parser('generate',
    description="Generate static file")
    generate_parser.set_defaults(func=generate_post)
    generate_parser.add_argument('title', type=clean_title, help="Title of post")
    generate_parser.add_argument("-a", "--author", default="Joe", help="Author of post")
    generate_parser.add_argument("-t", "--tags", default="", nargs="*", help="Tags of post")

    # Parser for deleting posts from posts dir and db
    delete_parser = subparsers.add_parser('delete',
    description="Delete static file")
    delete_parser.set_defaults(func=delete_post)
    delete_parser.add_argument('title', type=clean_title, help="Title of post")

    args = parser.parse_args()
    args.func(args)
