"""
Script for bulk publishing non-published posts in the directory
"""

import glob

from commands import publish_post
from commands.util import title_case
from data.db import get_db
from data.models import Post
from web.loggers import get_stderr_logger
from config import app_config

def bulk_publish_posts(args, logger):  # pylint: disable=W0613
    " Bulk publishes non-published posts from posts directory "

    def get_post_slugs_from_dir(dir_str=app_config.POSTS_DIR, ext_str=".md"):
        " Returns list of slugs based on filenames from a directory of posts "
        post_files = glob.glob(dir_str + "/*" + ext_str)

        return [t[len(dir_str) + 1:-len(ext_str)] for t in post_files]

    db = get_db()
    slugs = get_post_slugs_from_dir()
    unpublished_posts = db.session.query(Post).filter(Post.slug.in_(slugs))\
                                              .filter(~Post.published)
    num_unpub = unpublished_posts.count()

    if num_unpub > 0:
        for post in unpublished_posts:
            post.title = title_case(post.title)
            publish_post(post, logger, force=True)
        logger.info("Published {} posts!".format(num_unpub))
    else:
        logger.info("No unpublished posts found!")
