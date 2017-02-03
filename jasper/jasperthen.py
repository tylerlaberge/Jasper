from jasper.exceptions import ExpectationException
from jasper.utility import cyan, red, indent


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
            then_string = f'Then: {self.then_function.__name__}\n\n'
            exception_string = f'{self.exception.msg}\n'
            trace_location_string = f'{self.exception.relevant_trace[0]}\n'
            trace_code_string = indent(f'{self.exception.relevant_trace[1]}\n', 4)

            return red(then_string + exception_string + trace_location_string + trace_code_string)
