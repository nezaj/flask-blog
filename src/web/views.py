from flask import render_template, jsonify, abort, request

from web import app
from data.models import Post
from config import app_config
from util import convert

@app.route("/")
@app.route("/posts")
def posts():
    " Displays a list of posts "
    posts = app.db.session.query(Post).order_by(Post.published_dt.desc())
    page = convert(request.args.get('page'), int, 1)
    paginated_posts = posts.paginate(page=page, per_page=8)

    return render_template('/posts/index.tmpl', posts=paginated_posts)

@app.route("/posts/<string:slug>")
def post(slug):
    " Displays an individual post "
    post = app.db.session.query(Post).filter_by(slug=slug).first()
    if not post:
        abort(404)

    tags = ','.join([t.name for t in post.tags])
    prev_post = app.db.session.query(Post).filter(Post.id < post.id).order_by(Post.id.desc()).first()
    next_post = app.db.session.query(Post).filter(Post.id > post.id).order_by(Post.id.asc()).first()

    return render_template('/posts/show.tmpl', post=post, tags=tags,
                           prev_post=prev_post, next_post=next_post)

@app.route("/error")
def error_500():
    raise Exception("This is a fake error for testing purposes.")

# TODO: Turn this off when you do live delopyment
@app.route("/version")
def version():
    data = {
        "config": app_config.__name__,
        "debug": app.debug,
        "database": repr(app.db.engine.url),
        "posts_directory": app.config['POSTS_DIR']
    }
    return jsonify(data)
