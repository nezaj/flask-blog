import os

from commands.util import get_post_path, overwrite_file, slugify
from data.models import Post
from data.db import get_db

def generate_post(args, logger, force=False):
    """
    Generates a new file with a skeleton for the blog post and
    saves it into the static posts directory.

    The file name is the slug.md. If the file already exists
    user is prompted whether to overwrite the file.
    """
    post_path = get_post_path(args.title)

    # Check to see if file exists, if it does prompt for overwite
    if not force and os.path.isfile(post_path):
        if not overwrite_file(post_path):
            logger.info("{} was not re-generated".format(post_path))
            return

    # Prompt whether to delete post if already exists in db
    db = get_db()
    p = db.session.query(Post).filter_by(title=args.title).first()
    if p:
        if not force:
            resp = raw_input("Post with title '{}' already exists in db! Do you want to overwite (y/n)? ".format(args.title))
            if resp != 'y':
                logger.info("'{}' was not added to the db".format(args.title))
                return

        db.session.delete(p)
        db.session.commit()

    # Create post skeleton
    with open(post_path, 'w') as f:
        f.write("Author: {}\n".format(args.author))
        f.write("Title: {}\n".format(args.title))
        f.write("Tags: {}\n".format(', '.join(getattr(args, 'tags', ''))))
        f.write("\n") # Extra newline between metadata and content
        if args.content:
            f.write(args.content)

    logger.info("Generated new file at {}".format(post_path))

    # Create new post in db
    new_post = Post(author=args.author, title=args.title, slug=slugify(args.title))
    db.session.add(new_post)
    db.session.commit()
    logger.info("Added {} to the db!".format(new_post.title))
