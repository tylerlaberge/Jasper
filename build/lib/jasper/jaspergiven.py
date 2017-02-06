from jasper import Context
from jasper.utility import blue, red
from jasper.exceptions import GivenException


class Given(object):

    def __init__(self, function):
        self.given_function = function
        self.context = Context()
        self.passed = False

    def __call__(self, context):
        try:
            self.given_function(context)
        except Exception as e:
            raise GivenException(e)
        else:
            self.passed = True
            context.update(self.context)

    def __str__(self):
        color = blue if self.passed else red

        return color(f"Given: {self.given_function.__name__}")
