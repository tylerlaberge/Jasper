from jasper.utility import blue, red
from jasper.exceptions import GivenException
from functools import wraps
from collections import namedtuple


class Given(object):

    def __init__(self, function):
        self.given_function = function
        self.passed = False

    def __call__(self, context):
        try:
            self.given_function(context)
        except Exception as e:
            raise GivenException(e)
        else:
            self.passed = True

    def __str__(self):
        color = blue if self.passed else red

        return color(f"Given: {self.given_function.__name__}")


def given(func):
    @wraps(func)
    def wrapper(context):
        func(context)

    step = namedtuple('Step', ['cls', 'function'])
    return step(cls=Given, function=wrapper)

