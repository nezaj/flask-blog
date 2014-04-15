
"""
Helper functions for configuring our logging handlers.
"""

import logging

def configure_sqlalchemy_logger(format_string, level):
    logger = logging.getLogger('sqlalchemy.engine')
    logger.setLevel(level)
    logger.addHandler(get_stderr_handler(format_string, level))

def get_stderr_handler(format_string, level):
    """
    Returns a handler that outputs logged messages to standard error.
    """
    handler = logging.StreamHandler()
    handler.setLevel(level)
    handler.setFormatter(logging.Formatter(*format_string))
    return handler
