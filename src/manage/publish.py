from sqlalchemy import func
from web.db import get_db
from web.models import Post, Tag
from manage.util import get_post_path, slugify

def publish_post(args, force=False):
    # TODO: This function is doing a lot of things, let's clean it up

    def parse_attr(attr):
        return attr[attr.find(':') + 2:]

    def add_new_tags(tags):
        " Creates new tag models for tags that don't already exist in the db "
        new_tags = [Tag(name=t) for t in tags if not db.session.query(Tag).filter_by(name=t).first()]
        if new_tags:
            db.session.add_all(new_tags)
            db.session.commit()

    post_path = get_post_path(args.title)

    # Open the file and extract attributes
    try:
        with open(post_path, 'r') as f:
            author = f.readline().strip('n')
            title = f.readline().strip('\n')
            tags = f.readline().strip('\n')
            _ = f.readline() # throw-away line
            content = f.read()
    except IOError:
        print "Error: Could not find {}".format(post_path)
        return

    # Process attributes
    author = parse_attr(author)
    title = parse_attr(title)
    slug = slugify(title)
    tags = parse_attr(tags).split(',')
    if '' in tags:
        tags.remove('')

    # Prompt whether to delete post if already exists in db
    db = get_db()
    p = db.session.query(Post).filter_by(title=title).first()
    if not force and p:
        resp = raw_input("Post with title '{}' already exists! Do you want to overwite (y/n)? ".format(title))
        if resp != 'y':
            print "'{}' was not added to the db".format(title)
            return
        else:
            db.session.delete(p)
            db.session.commit()

    # Create post object
    new_post = Post(author=author, title=title, slug=slug, content=content, published_dt=func.now())

    # Assign tags to post
    if tags:
        add_new_tags(tags)
        tags = [db.session.query(Tag).filter_by(name=t).first() for t in tags]
        new_post.tags = tags

    # Commit to db
    db.session.add(new_post)
    db.session.commit()
    print "Added {} to the db!".format(title)
