#!/usr/bin/env python

import argparse
import os
import subprocess

from config import app_config
from data.db import DatabaseConnection
from util import parse_sqlalchemy_url

def yes_no(message):
    response = raw_input("{} [y/n] ".format(message))
    while response.lower() not in ['y', 'n']:
        response = raw_input("Please enter 'y' or 'n'. ")
    return response == 'y'

def build_named_arglist(arg_dict):
    for name, value in arg_dict.iteritems():
        yield "--{}".format(name)
        yield str(value)

def invoke_process(proc_name, proc_args, **subprocess_args):
    return subprocess.call([proc_name] + proc_args, **subprocess_args)

def build(args):
    db = DatabaseConnection(args.url)
    print u"Connected to {}.".format(repr(db.engine.url))
    if yes_no("Are you sure you want to build the database?"):
        from data.prepare import build_db
        print "Building database..."
        build_db(db.engine)

def prepopulate(args):  # pylint: disable=W0613
    if yes_no("Are you sure you want to prepopulate the database with sample data?"):
        from data.prepare import prepopulate_db
        print "Prepopulating databsae..."
        prepopulate_db()

def repl(args):
    dialect = args.url.get_dialect()
    if dialect.name == "postgresql":
        env = os.environ.copy()
        env["PGPASSWORD"] = args.url.password
        proc_args = list(build_named_arglist({
            'host': args.url.host,
            'port': args.url.port,
            'username': args.url.username,
            'dbname': args.url.database
        }))
        return invoke_process("psql", proc_args, env=env)
    elif dialect.name == "sqlite":
        proc_args = [args.url.database] if args.url.database else []
        return invoke_process("sqlite3", proc_args)
    else:
        raise argparse.ArgumentTypeError("Dialect {} is not supported.".format(dialect.name))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Tools for updating or migrating the database schema.')
    parser.add_argument('--url',
                        type=parse_sqlalchemy_url,
                        default=app_config.SQLALCHEMY_DATABASE_URI,
                        help="A RFC1738 URL to a PostgreSQL or SQLite database to use.")
    subparsers = parser.add_subparsers()

    build_parser = subparsers.add_parser('build', description="""
    Build the database with tables defined in metadata
    """)
    build_parser.set_defaults(func=build)

    prepopulate_parser = subparsers.add_parser('prepopulate', description="""
    Prepopulate the database with sample data
    """)
    prepopulate_parser.set_defaults(func=prepopulate)

    repl_parser = subparsers.add_parser('repl', description="""
    Launch a psql or sqlite repl connected to the database.
    """)
    repl_parser.set_defaults(func=repl)

    args = parser.parse_args()
    args.func(args)
