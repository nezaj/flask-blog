#!/usr/bin/env python

" Script to generate new blog posts "

import argparse
import os
from util import clean_title

static_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'web/static/posts')


def write_file_template(file_path, args):
    " Creates a skeleton file based on the file path "

    with open(file_path, 'w') as f:
        f.write("Author: {}\n".format(args.author))
        f.write("Title: {}\n".format(args.title))
        f.write("\n") # Extra newline at the end

def overwrite_file(file_name):
    "Prompt for overwriting a file"

    resp = raw_input("{} already exists! Do you want to overwrite (y/n)? ".format(file_name))
    if resp != 'y':
        print "{} was not re-generated".format(file_name)
        return False
    else:
        return True

def generate_post(args):
    """
    Generates a new file with a skeleton for the blog post and
    saves it into the static directory.

    The file name is based on the title of the blog post. If
    the file already exists user is prompted whether to
    overwrite the file.
    """

    file_name = args.title.replace(' ', '_').lower() + ".txt"
    file_path = os.path.join(static_directory, file_name)

    if os.path.isfile(file_path):
        if not overwrite_file(file_name): return

    write_file_template(file_path, args)
    print "Generated file {} in {}".format(file_name, static_directory)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Tool for generating posts")
    parser.set_defaults(func=generate_post)

    parser.add_argument('title', type=clean_title, help="Title of post")
    parser.add_argument("-a", "--author", default="nezaj", help="Author of post")

    args = parser.parse_args()
    args.func(args)
