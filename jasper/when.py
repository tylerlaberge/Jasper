from jasper.utility import blue, red, grey
from jasper.exceptions import WhenException
from functools import wraps


class When(object):

    def __init__(self, function):
        self.when_function = function
        self.context = None
        self.passed = False

    def __call__(self, context):
        self.context = context
        try:
            self.when_function(self.context)
        except Exception as e:
            raise WhenException(e)
        else:
            self.passed = True

    def __str__(self):
        if not self.context:
            color = grey
        elif self.passed:
            color = blue
        else:
            color = red

        return color(f'When: {self.when_function.__name__}')


def when(func):
    @wraps(func)
    def wrapper(context):
        func(context)

    return When(wrapper)
