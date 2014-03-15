"""
Templating rendering helper functions, e.g. custom tests & filters,
and infrastructure for enumerating and loading templates
"""

from flask import Markup
import misaka
from markdown import markdown
from web import app

@app.template_filter()
def markdownize(content):
    " Converts Markdown content into html "
    return Markup(misaka.html(content))
