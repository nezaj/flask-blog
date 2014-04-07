import os

from sqlalchemy import func
from data.db import DatabaseConnection, get_db
from data.models import Post, Tag
from manage.util import get_post_path, slugify

def publish_post(args, force=False):
    # TODO: I'm really not happy with function. It should be split up

    def parse_attr(attr):
        return attr[attr.find(':') + 2:]

    def get_new_tags(tag_name_list):
        return [Tag(name=t) for t in tag_name_list if not db.session.query(Tag).filter_by(name=t).first()]

    def get_tags(tag_name_list):
        return [db.session.query(Tag).filter_by(name=t).first() for t in tag_name_list]

    # Prompt whether to delete post if already exists in db
    title = args.title

    # TODO: This seems like a hack, there may be a better way
    if hasattr(args, 'prod') and args.prod:
        db = DatabaseConnection(os.environ.get('HEROKU_BLOG'))
    else:
        db = get_db()

    p = db.session.query(Post).filter_by(title=title).first()

    if p:
        if not force:
            resp = raw_input("Post with title '{}' already exists! Do you want to overwite (y/n)? ".format(args.title))
            if resp != 'y':
                print "'{}' was not added to the db".format(args.title)
                return

        db.session.delete(p)
        db.session.commit()

    # Open the file and extract attributes
    post_path = get_post_path(args.title)
    try:
        with open(post_path, 'r') as f:
            author = f.readline().strip('n')
            _ = f.readline() # Title line, don't need
            tags = f.readline().strip('\n')
            _ = f.readline() # Line seperating content, don't need
            content = f.read()
    except IOError:
        print "Error: Could not find {}".format(post_path)
        return

    # Process attributes
    author = parse_attr(author)
    slug = slugify(title)
    tags = parse_attr(tags).split(', ')
    if '' in tags:
        tags.remove('')

    # Create post object
    new_post = Post(author=author, title=title, slug=slug, content=content, published_dt=func.now())

    # Assign tags to post
    if tags:
        new_tags = get_new_tags(tags)
        db.session.add_all(new_tags)
        db.session.commit()

        tags = get_tags(tags)
        new_post.tags = tags

    # Commit to db
    db.session.add(new_post)
    db.session.commit()
    print "Added {} to the db!".format(title)
