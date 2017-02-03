from jasper.exceptions import ExpectationException, ThenException
from jasper.utility import cyan, red, grey


class JasperThen(object):

    def __init__(self, function_name):
        self.then_function = getattr(self, function_name)
        self.context = None
        self.passed = False

    def __call__(self, context):
        self.context = context

        try:
            self.then_function()
        except ExpectationException as e:
            raise ThenException(e)
        else:
            self.passed = True

    def __str__(self):
        if not self.context:
            color = grey
        elif self.passed:
            color = cyan
        else:
            color = red

        return color(f'Then: {self.then_function.__name__}')
