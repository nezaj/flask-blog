from sqlalchemy import func

from config import app_config
from data.db import get_db
from data.models import Post
from commands.backup import make_backup
from commands.util import get_tags, get_new_tags, parse_attr, \
                          get_post_path, slugify

def publish_post(args, logger):
    """
    Extracts and updates db post model with metadata from static post file.

    Uses the post title and env defined post directory to locate which static file
    to use. This is done for convenience so a user can simply type in the name of
    their post instead of a full file path.

    Sets published_dt to time when this function is run. Also adds new tags to the
    db if they did not already exist.
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

    # Backup posts in production before publishing
    if app_config.ENV == 'prod':
        make_backup(app_config.POSTS_DIR, app_config.BACKUP_POSTS_DIR, logger)

    # Update post object
    db = get_db()
    publish_post = db.session.query(Post).filter_by(title=args.title)
    publish_post.update({
        "author": author,
        "title": args.title,
        "slug": slug,
        "content": content,
        "published_dt": func.now()
    }, synchronize_session=False)
    db.session.commit()

    if tags:
        # Add new tags to db
        new_tags = get_new_tags(db, tags)
        db.session.add_all(new_tags)
        db.session.commit()

        # Assign tags to post
        tags = get_tags(db, tags)
        post_obj = publish_post.first()
        post_obj.tags = tags
        db.session.add(post_obj)
        db.session.commit()

    logger.info("Published {}!".format(args.title))
