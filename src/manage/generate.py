import os

from manage.util import get_post_path, overwrite_file

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

    # Create post skeleton
    with open(post_path, 'w') as f:
        f.write("Author: {}\n".format(args.author))
        f.write("Title: {}\n".format(args.title))
        f.write("Tags: {}\n".format(', '.join(getattr(args, 'tags', ''))))
        f.write("\n") # Extra newline between metadata and content
        if args.content:
            f.write(args.content)

    logger.info("Generated new file at {}".format(post_path))
