from jasper.exceptions import ExpectationException, ThenException
from jasper.utility import blue, red, grey


class Then(object):

    def __init__(self, function):
        self.then_function = function
        self.context = None
        self.passed = False

    def __call__(self, context):
        self.context = context

        try:
            self.then_function(self.context)
        except ExpectationException as e:
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
