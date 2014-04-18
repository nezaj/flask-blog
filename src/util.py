"""
Useful functions for generic use
"""

import sys
import argparse

from sqlalchemy.engine.url import make_url

def convert(value, to_type, default=None):
    """
    Attempts to convert a given value to a new type by calling the
    type constructor.  If the coercion throws an exception, return the
    default value.
    """
    try:
        return to_type(value)
    except Exception:  # pylint: disable=W0703
        return default


def parse_sqlalchemy_url(input_url):
    """
    Parses the input as a valid SQLAlchemy URL, or otherwise raises an
    exception that argparse will recognize as a type validation error.
    """
    try:
        url = make_url(input_url)
        _ = url.get_dialect()  # may throw if the URI refers to a mystery dialect
        return url
    except Exception as e:
        _, e, tb = sys.exc_info()
        raise argparse.ArgumentTypeError, argparse.ArgumentTypeError(str(e)), tb
