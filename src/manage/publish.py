from sqlalchemy import func
from web import app
from web.models import Post, Tag
from util import get_post_path, slugify

def publish_post(args, force=False):

    # TODO: This function is doing a lot of things, let's clean it up

    def parse_attr(attr):
        return attr[attr.find(':') + 2:]

    # TODO: This should go somewhere else
    def add_new_tags(tags):
        new_tags = [Tag(name=t) for t in tags if not app.db.session.query(Tag).filter_by(name=t).first()]
        if new_tags:
            app.db.session.add_all(new_tags)
            app.db.session.commit()

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
    p = app.db.session.query(Post).filter_by(title=title).first()
    if not force and p:
        resp = raw_input("Post with title '{}' already exists! Do you want to overwite (y/n)? ".format(title))
        if resp != 'y':
            print "'{}' was not added to the db".format(title)
            return
        else:
            app.db.session.delete(p)
            app.db.session.commit()

    # Create post object
    new_post = Post(
        author=author,
        title=title,
        slug=slug,
        content=content,
        published_dt=func.now()
        )

    # Assign tags to post
    if tags:
        add_new_tags(tags)
        tags = [app.db.session.query(Tag).filter_by(name=t).first() for t in tags]
        new_post.tags = tags

    # Commit to db
    app.db.session.add(new_post)
    app.db.session.commit()
    print "Added {} to the db!".format(title)

