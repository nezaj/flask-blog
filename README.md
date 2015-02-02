## Flask Blog
My personal blogging platform. Made with [Flask][flask]. Uses simple command line tools to manage and publish posts. Supports tagging, drafting, and backing-up posts.

### Quickstart
```
git clone git@github.com:nezaj/flask-blog.git
sudo pip install virtualenv
make virtualenv
source ~/.virtualenvs/blog/bin/activate
cd src
./sql.py build  # Build the database
./run.py  # Runs the development server
```

Now go to [http://localhost:5000/][localhost] in your favorite browser. Huzzah!

### Quick Example
From the root directory, use the following to generate a new post
```
v blog  # If you don't already have the virtualenv activcated
cd src
./manage_posts.py generate "Sample Post"
```

This will create a skeleton markdown file in the `src/posts` directory. To see a full list of options for the `generate` command type `./manage_posts.py generate -h`

You can publish the file locally using the **publish** command
```
./manage_posts.py publish "Sample Post"
```
If you invoke `./run.py` and go to `localhost:5000` the post should now appear.

When you ready to publish it live set `CONFIG_ENV` to `prod`
```
CONFIG_ENV=prod ./manage_posts.py publish "Sample Post"
```
You can also publish posts as drafts (accesible by direct URL only) via
```
CONFIG_ENV=prod ./manage_posts.py publish "Sample Post" -d`
```

See the `src/commands` directory for a full list of commands

[flask]: http://flask.pocoo.org/
[localhost]: http://localhost:5000/
