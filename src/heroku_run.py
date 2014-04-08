#!/usr/bin/env python

" Used by gunicorn in heroku deployment "

# Gunicorn uses app
# pylint: disable=W0611
from web import app
