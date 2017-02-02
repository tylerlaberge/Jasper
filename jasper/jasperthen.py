from jasper.exceptions import ExpectationException


class JasperThen(object):

    def __init__(self, function_name):
        self.then_function = getattr(self, function_name)

    def __call__(self, context):
        self.context = context

        try:
            self.then_function()
        except ExpectationException:
            self.context.success = False
        else:
            self.context.success = True
