"""
Helpers for running manage_posts commands.
"""

import os
import re
from unicodedata import normalize

from config import app_config
from data.models import Tag

# Regex for slugify
_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')

def get_tags(db, tag_name_list):
    " Returns a list of Tag models from the given list of tag names "
    return [db.session.query(Tag).filter_by(name=t).first() for t in tag_name_list]

def get_new_tags(db, tag_name_list):
    " Returns a list of Tag models that don't already exist in the db "
    return [Tag(name=t) for t in tag_name_list if not db.session.query(Tag).filter_by(name=t).first()]

def get_post_path(post_title):
    " Returns path of a post "
    file_name = slugify(post_title) + ".md"
    return os.path.join(app_config.POSTS_DIR, file_name)

def overwrite_file(file_path):
    " Bool representing whether to overwrite a file. "
    resp = raw_input("{} already exists! Do you want to overwrite (y/n)? ".format(file_path))
    return True if resp == 'y' else False

def parse_attr(attr):
    " Used for parsing metadata in post files "
    return attr[attr.find(':') + 2:]

def slugify(text, delim=u'-'):
    """
    Generates an ASCII-only slug.
    Thanks to this snippet http://flask.pocoo.org/snippets/5/
    """
    result = []
    text = unicode(text) if not isinstance(text, unicode) else text
    for word in _punct_re.split(text.lower()):
        word = normalize('NFKD', word).encode('ascii', 'ignore')
        if word:
            result.append(word)

    return unicode(delim.join(result))

def title_case(t):
    " Title cases a string "
    return t.title()
