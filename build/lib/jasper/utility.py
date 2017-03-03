"""
The utility module.
"""

import traceback


def extract_traceback(exception):
    """
    Utility function for extracting the traceback from an exception.

    :param exception: The exception to extract the traceback from.
    :return: The extracted traceback.
    """
    return ''.join(traceback.format_tb(exception.__traceback__))



