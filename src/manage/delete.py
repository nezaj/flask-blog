import os
from data.db import get_db
from data.models import Post
from manage.util import get_post_path

def delete_post(args):
    """
    Removes post specified by title from posts directory directory and
    from the db
    """

    def delete_from_dir(title):
        post_path = get_post_path(title)
        if os.path.isfile(post_path):
            os.remove(post_path)
            print "Removed {}".format(post_path)
        else:
            print "Error: Could not find {}".format(post_path)

    def delete_from_db(title):
        post_model = db.session.query(Post).filter(Post.title == args.title).first()
        if post_model:
            db.session.delete(post_model)
            db.session.commit()
            print 'Removed "{}" from the db'.format(title)
        else:
            print 'Error: Could not find "{}" in the db'.format(title)

    db = get_db()
    delete_from_dir(args.title)
    delete_from_db(args.title)
