"""
Script for bulk publishing non-published posts in the directory
"""

from commands import publish_post
from commands.util import title_case
from data.db import get_db
from data.models import Post

def bulk_publish_posts(args, logger):  # pylint: disable=W0613
    " Publish all non-published posts from static posts directory "
    db = get_db()
    unpublished_posts = db.session.query(Post).filter(~Post.published)
    num_unpub = unpublished_posts.count()

    if num_unpub > 0:
        for post in unpublished_posts:
            post.title = title_case(post.title)
            publish_post(post, logger)
        logger.info("Bulk publish complete -- published {} posts!".format(num_unpub))
    else:
        logger.info("Bulk publish complete -- no unpublished posts found!")
