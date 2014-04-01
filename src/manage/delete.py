
import os
from web import app
from web.models import Post
from util import get_post_path

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
        post_model = app.db.session.query(Post).filter(Post.title == args.title).first()
        if post_model:
            app.db.session.delete(post_model)
            app.db.session.commit()
            print "Remove {}".format(post_model)
        else:
            print 'Error: Could not find "{}" in the db'.format(title)

    delete_from_dir(args.title)
    delete_from_db(args.title)
