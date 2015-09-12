#!/usr/bin/env python

"""
Usage: ./manage_posts <command> [<args>]
Parsers for managing posts. Currently supported commands are:

- generate <args>: Creates a new static file in folder directory
- publish <args>: Adds a static file to the db
- delete <args>: Deletes specified file from static folder and db
- backup <args>: Backs-up post directory to specified backup directory
                 make sure you explicitly define this. Currently will
                 use POSTS_DIR defined by BaseConfig. We don't ever need
                 to backup posts from the test directory

- bulk_publish: Publishes all unpublished posts
- list: Lists published/unpublished posts
"""

import argparse
import os

from config.settings import BaseConfig
from commands import generate_post, publish_post, \
                     list_posts, delete_post, backup_posts, \
                     bulk_publish_posts
from commands.util import title_case
from loggers import get_stderr_logger

def import_env():
    if os.path.exists('.env'):
        print 'Importing environment from .env...'
        for line in open('.env'):
            var = line.strip().split('=', 1)
            if len(var) == 2:
                os.environ[var[0]] = var[1]

if __name__ == '__main__':
    import_env()

    parser = argparse.ArgumentParser(description="Tools for managing posts")
    subparsers = parser.add_subparsers()

    # Parser for listing published and unpublished files
    list_parser = subparsers.add_parser('list', description="List published and unpublished files")
    list_parser.set_defaults(func=list_posts)

    # Parser for adding static files to db
    publish_parser = subparsers.add_parser('publish', description="Publish static file")
    publish_parser.set_defaults(func=publish_post)
    publish_parser.add_argument('title', type=title_case, help="Title of post")
    publish_parser.add_argument("--draft", "-d", action="store_true",
                                default=False, help="Flag for draft publishing a post")

    # Parser for bulk publishing static files
    bulk_publish_parser = subparsers.add_parser('bulk_publish',
                                                description="Bulk publish static files in posts directory")
    bulk_publish_parser.set_defaults(func=bulk_publish_posts)

    # Parser for generating static files
    generate_parser = subparsers.add_parser('generate', description="Generate static file")
    generate_parser.set_defaults(func=generate_post)
    generate_parser.add_argument('title', type=title_case, help="Title of post")
    generate_parser.add_argument("-a", "--author", default="nezaj", help="Author of post")
    generate_parser.add_argument("-t", "--tags", default="", nargs="*", help="Tags of post")
    generate_parser.add_argument("-c", "--content", default="\n", help="Post content")

    # Parser for deleting posts from posts dir and db
    delete_parser = subparsers.add_parser('delete', description="Delete static file")
    delete_parser.set_defaults(func=delete_post)
    delete_parser.add_argument('title', type=title_case, help="Title of post")

    # Parser for backing up posts
    backup_parser = subparsers.add_parser('backup', description="Backup post files")
    backup_parser.set_defaults(func=backup_posts)
    backup_parser.add_argument("-s", "--src", default=BaseConfig.POSTS_DIR, help="Source directory for posts to backup")
    backup_parser.add_argument("-t", "--tgt", default=BaseConfig.BACKUP_POSTS_DIR, help="Title of post")

    args = parser.parse_args()
    logger = get_stderr_logger()

    args.func(args, logger)
