from functools import wraps
from jasper.utility import cyan, red, grey
from jasper.exceptions import WhenException


class JasperWhen(object):

    def __init__(self, function_name):
        self.when_function = getattr(self, function_name)
        self.context = None
        self.passed = False

    def __call__(self, context):
        self.context = context

        try:
            self.when_function()
        except Exception as e:
            raise WhenException(e)
        else:
            self.passed = True

    def __str__(self):
        if not self.context:
            color = grey
        elif self.passed:
            color = cyan
        else:
            color = red

        return color(f'When: {self.when_function.__name__}')
