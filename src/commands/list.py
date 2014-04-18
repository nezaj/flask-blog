from data.db import get_db
from data.models import Post

def list_posts(args, logger):  # pylint: disable=W0613
    " List published and unpublished posts "

    def display_posts(posts):
        for p in posts:
            print p.title

    db = get_db()
    published_posts = db.session.query(Post).filter(Post.published).order_by(Post.published_dt.desc())
    unpublished_posts = db.session.query(Post).filter(~Post.published)

    # Print and format published posts
    div = "="*20
    print '\n{}\nPublished Posts:\n{}\n'.format(div, div)
    if published_posts:
        display_posts(published_posts)

    # Print and format unpublished posts
    print '\n{}\nUnpublished Posts:\n{}\n'.format(div, div)
    if unpublished_posts:
        display_posts(unpublished_posts)
