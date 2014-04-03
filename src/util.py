"""
Useful functions for generic use
"""

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
