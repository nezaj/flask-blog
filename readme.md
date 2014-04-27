## Flask Blog
A light-weight blogging platform written in Flask. Use simple command line tools to manage and publish posts. Supports tagging, drafting, and backing-up posts.

* [Getting Started](#getting-started)

### Getting Started
Flask Blog was built and tested in Python 2 exclusively. Before trying to make a [virtualenv][venv-docs], you should make sure that Python 2.7 is your system's default Python, and that [pip][pip-docs] is a Python 2 version of pip. (If that's not the case, you should uninstall and reinstall pip -- see the install directions on its [website][pip-docs].)
```
$ python --version
Python 2.7.3
$ pip --version
pip 1.1 from ~/.virtualenvs/rads/lib/python2.7/site-packages/pip-1.1-py2.7.egg (python 2.7)
```
Next you should build a [virtualenv][venv-docs] to contain this project's Python dependencies. The Makefile will create one for you and put it in `~/.virtualenvs/blog`. If you get strange errors during this step, check that you don't have Python 3 `python`, `pip`, or `virtualenv` in your `PATH`.
```
sudo pip install virtualenv
make virtualenv
```
Then activate it:
```
source ~/.virtualenvs/blog/bin/activate
```
Instead of activating it manually like that, you might find it convenient to use [virtualenvwrapper][venv-wrapper-docs] for working with virtualenvs (recommended):
```
sudo pip install virtualenvwrapper
source /usr/local/bin/virtualenvwrapper.sh
workon blog
```
If you ever need to upgrade it or install packages which appeared since your last run, just run `make virtualenv` again.

[venv-docs]: http://docs.python-guide.org/en/latest/dev/virtualenvs/
[pip-docs]: http://pip.readthedocs.org/
[venv-wrapper-docs]: http://virtualenvwrapper.readthedocs.org/en/latest/
