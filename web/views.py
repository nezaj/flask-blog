from flask import render_template, Markup
from web import app
from web.models import Post
from markdown import markdown

@app.route("/")
@app.route("/posts")
def posts():
    " Displays a list of posts "
    posts = Post.query.order_by(Post.published_dt.desc())
    return render_template('/posts/index.tmpl', posts=posts)

@app.route("/posts/<string:slug>")
def post(slug):
    " Displays an individual post "
    post = Post.query.filter_by(slug=slug).first_or_404()
    return render_template('/posts/show.tmpl', post=post)

@app.route("/error")
def error_500():
    raise Exception("This is a fake error for testing purposes.")
