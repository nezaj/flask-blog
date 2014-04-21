from sqlalchemy import func

from config import app_config
from data.db import get_db
from data.models import Post
from commands.backup import make_backup
from commands.util import get_tags, get_new_tags, parse_attr, \
                          get_post_path, slugify

def publish_post(args, logger):
    """
    Persists post to database based on passed args and metadata from static
    post file. A post can be considered "published" once this function is run.

    There are two types of publishing:

    Normal -- sets published_dt to the current time. This post will be
              listed in the posts index and will be included in previous/next
              links.

     Draft -- sets published_dt to None. This post will not appear in the posts
              index and will not be included in previous/next links. However,
              this post can still be viewed through the slug url. This is
              useful if you want to publish your post for select review
              without displaying a link for everyone to see.

    In both cases the post model will be updated and committed to the db. Also,
    new tag models are created if a post includes tags that do not already exist
    in the db.

    Note: We use the post title and env defined post directory to locate which
    static file to use. This is done for convenience so a user can simply type
    in the name of their post instead of a full file path.
    """
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
        logger.info("Error: Could not find {}".format(post_path))
        return

    # Process attributes
    author = parse_attr(author)
    slug = slugify(args.title)
    tags = parse_attr(tags).split(', ')
    if '' in tags:
        tags.remove('')

    # If this is a draft post, don't set the publish date
    published_dt = None if args.draft else func.now()

    # Backup posts in production
    if app_config.ENV == 'prod':
        make_backup(app_config.POSTS_DIR, app_config.BACKUP_POSTS_DIR, logger)

    # Create post in db
    db = get_db()
    new_post = Post(author=author, title=args.title, slug=slug,
                    content=content, published_dt=published_dt)
    db.session.add(new_post)
    db.session.commit()

    if tags:
        # Add new tags to db
        new_tags = get_new_tags(db, tags)
        db.session.add_all(new_tags)
        db.session.commit()

        # Assign tags to post
        tags = get_tags(db, tags)
        new_post.tags = tags
        db.session.add(new_post)
        db.session.commit()

    action_msg = "Draft published" if args.draft else "Published"
    logger.info("{} {}!".format(action_msg, args.title))
