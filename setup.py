#!/usr/bin/env python

from setuptools import setup, find_packages

dependencies = [
    "pep8",
    "pylint",
    "nose==1.3.0",
    "cssmin==0.2.0",
    "pyscss==1.2.0",
    "grip",
    "misaka==1.0.2",
    "gunicorn==0.17.2",
    "sqlalchemy==0.9.3",
    "flask==0.10.1",
    "flask-assets==0.9",
    "alembic==0.6.3",
    "psycopg2==2.5.2",
]

setup(
    name="flask-blog",
    version="0.1dev",
    url="https://github.com/nezaj/flask-blog",
    packages=find_packages(),
    zip_safe=False,
    install_requires=dependencies
)
