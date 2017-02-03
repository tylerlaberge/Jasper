from jasper.exceptions import ExpectationException
from jasper.utility import cyan, red
import traceback


class JasperThen(object):

    def __init__(self, function_name):
        self.then_function = getattr(self, function_name)
        self.exception = None

    def __call__(self, context):
        self.context = context

        try:
            self.then_function()
        except ExpectationException as e:
            self.context.success = False
            self.exception = e
        else:
            self.context.success = True

    def __str__(self):
        if self.context.success:
            return cyan(f'Then: {self.then_function.__name__}')
        else:
            return red(f'Then: {self.then_function.__name__}\n\n        '
                       f'{self.exception.msg}\n        '
                       f'{self.exception.relevant_trace[0]}\n            '
                       f'{self.exception.relevant_trace[1]}\n')
