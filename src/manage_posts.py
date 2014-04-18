#!/usr/bin/env python

"""
Parsers for managing posts. Currently supported commands are:
Usage: ./manage_posts <command> <args>

- generate <args>: Creates a new static file in folder directory
- publish <args>: Adds a static file to the db
- list: Lists published/unpublished posts
- delete <args>: Deletes specified file from static folder and db
- backup <args>: Backs-up post directory to specified backup directory
                 make sure you explicitly define this. Currently will
                 use POSTS_DIR defined by DevConfig. We don't ever need
                 to backup posts from the test directory
"""

import os
import argparse

from config import DevConfig
from commands import generate_post, publish_post, \
                     list_posts, delete_post, backup_posts, \
                     bulk_publish_posts
from commands.util import title_case
from web.loggers import get_stderr_logger

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Tools for managing posts")
    subparsers = parser.add_subparsers()

    # Parser for listing published and unpublished files
    list_parser = subparsers.add_parser('list', description="List published and unpublished files")
    list_parser.set_defaults(func=list_posts)

    # Parser for adding static files to db
    publish_parser = subparsers.add_parser('publish', description="Publish static file")
    publish_parser.set_defaults(func=publish_post)
    publish_parser.add_argument('title', type=title_case, help="Title of post")
    publish_parser.add_argument("--prod", action="store_true",
                                default=False, help="Flag for publishing to production db")

    # Parser for bulk publishing static files
    bulk_publish_parser = subparsers.add_parser('bulk_publish', description="Bulk publish static files in posts directory")
    bulk_publish_parser.set_defaults(func=bulk_publish_posts)

    # Parser for generating static files
    generate_parser = subparsers.add_parser('generate', description="Generate static file")
    generate_parser.set_defaults(func=generate_post)
    generate_parser.add_argument('title', type=title_case, help="Title of post")
    generate_parser.add_argument("-a", "--author", default="nezaj", help="Author of post")
    generate_parser.add_argument("-t", "--tags", default="", nargs="*", help="Tags of post")
    generate_parser.add_argument("-c", "--content", help="Post content")

    # Parser for deleting posts from posts dir and db
    delete_parser = subparsers.add_parser('delete', description="Delete static file")
    delete_parser.set_defaults(func=delete_post)
    delete_parser.add_argument('title', type=title_case, help="Title of post")

    # Parser for backing up posts
    backup_parser = subparsers.add_parser('backup', description="Backup post files")
    backup_parser.set_defaults(func=backup_posts)
    backup_parser.add_argument("-s", "--src", default=DevConfig.POSTS_DIR, help="Source directory for posts to backup")

    posts_backup_dir = os.path.join(os.path.expanduser('~'), 'backup/blog_posts')
    backup_parser.add_argument("-t", "--tgt", default=posts_backup_dir, help="Title of post")

    args = parser.parse_args()
    logger = get_stderr_logger()

    args.func(args, logger)
