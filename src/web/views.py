from flask import render_template, jsonify, abort
from web import app
from data.models import Post
from config import app_config

@app.route("/")
@app.route("/posts")
def posts():
    " Displays a list of posts "
    posts = app.db.session.query(Post).order_by(Post.published_dt.desc())
    return render_template('/posts/index.tmpl', posts=posts)

@app.route("/posts/<string:slug>")
def post(slug):
    " Displays an individual post "
    post = app.db.session.query(Post).filter_by(slug=slug).first()
    if not post:
        abort(404)

    tags = ','.join([t.name for t in post.tags])
    return render_template('/posts/show.tmpl', post=post, tags=tags)

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
