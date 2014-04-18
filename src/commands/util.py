" Helpers for scripts "

import os
import re
from unicodedata import normalize
from config import app_config

# Regex for slugify
_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')

def title_case(t):
    " Title cases a string "
    return t.title()

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

def get_post_path(post_title):
    " Returns path of a post "

    file_name = slugify(post_title) + ".md"
    return os.path.join(app_config.POSTS_DIR, file_name)

def overwrite_file(file_path):
    """
    Bool representing whether to overwrite a file.
    Returns True if user responsed with y else False
    """

    resp = raw_input("{} already exists! Do you want to overwrite (y/n)? ".format(file_path))
    return True if resp == 'y' else False
