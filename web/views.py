from flask import render_template, Markup
from web import app
from web.models import Post
from markdown import markdown

def clean_contents(c):
    " Helper for cleaning contents of blog post "
    def replace_newlines(s):
        return s.replace('\n', '<br />')

    c = replace_newlines(c)
    return c

@app.route("/")
@app.route("/posts")
def posts():
    " Displays a list of posts "
    posts = Post.query.all()
    return render_template('/posts/index.tmpl', posts=posts)

@app.route("/posts/<string:title>")
def post(title):
    " Displays an individual post "
    post = Post.query.filter_by(title=title).first_or_404()
    content = clean_contents(post.content)
    return render_template('/posts/show.tmpl', post=post, content=content)
