from jasper.exceptions import ThenException
from jasper.utility import blue, red, grey
from functools import wraps


class Then(object):

    def __init__(self, function):
        self.then_function = function
        self.context = None
        self.passed = False

    def __call__(self, context):
        self.context = context
        try:
            self.then_function(self.context)
        except Exception as e:
            raise ThenException(e)
        else:
            self.passed = True

    def __str__(self):
        if not self.context:
            color = grey
        elif self.passed:
            color = blue
        else:
            color = red

        return color(f'Then: {self.then_function.__name__}')


def then(func):
    @wraps(func)
    def wrapper(context):
        func(context)

    return Then(wrapper)
