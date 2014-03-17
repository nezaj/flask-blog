#!/usr/bin/env python
from web import db
from publish import publish_post

def prepopulate():
    publish_post('lorem.md')

if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    prepopulate()
    print 'database rebuilt!'
