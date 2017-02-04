from jasper import Context
from jasper.utility import cyan, red
from jasper.exceptions import GivenException


class JasperGiven(object):

    def __init__(self, function_name):
        self.given_function = getattr(self, function_name)
        self.context = Context()
        self.passed = False

    def __call__(self, context):
        try:
            self.given_function()
        except Exception as e:
            raise GivenException(e)
        else:
            self.passed = True
            context.update(self.context)

    def __str__(self):
        color = cyan if self.passed else red

        return color(f"Given: {self.given_function.__name__}")
