from flask import render_template
from web import app
from web.models import Post

@app.route("/")
@app.route("/posts")
def index():
    posts = Post.query.all()
    return render_template('/posts/index.tmpl', posts=posts)

@app.route("/posts/<string:title>")
def post(title):
    post = Post.query.filter_by(title=title).first_or_404()
    return render_template('/posts/show.tmpl', post=post)
