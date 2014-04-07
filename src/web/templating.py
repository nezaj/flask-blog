"""
Templating rendering helper functions, e.g. custom tests & filters,
and infrastructure for enumerating and loading templates
"""

from flask import Markup
from datetime import datetime
import misaka
from web import app

@app.template_filter()
def markdownize(content):
    " Converts Markdown content into html "
    # pylint can't recognize misaka.html
    # pylint: disable=E1101
    return Markup(misaka.html(content))
