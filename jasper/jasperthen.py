from jasper.exceptions import ExpectationException, ThenException
from jasper.utility import cyan, red, grey


class JasperThen(object):

    def __init__(self, function_name):
        self.then_function = getattr(self, function_name)
        self.context = None

    def __call__(self, context):
        self.context = context

        try:
            self.then_function()
        except ExpectationException as e:
            self.context.success = False
            raise ThenException(e)
        else:
            self.context.success = True

    def __str__(self):
        if not self.context:
            color = grey
        elif self.context.success:
            color = cyan
        else:
            color = red

        return color(f'Then: {self.then_function.__name__}')
