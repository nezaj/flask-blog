#!/usr/bin/env python

" Run dev version of webserver "

from web import app
app.run(debug = True)
