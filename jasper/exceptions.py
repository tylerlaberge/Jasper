class ExpectationException(Exception):

    def __init__(self, actual, expected, operator):
        super().__init__()
        self.actual = actual
        self.expected = expected
        self.operator = operator

    def __str__(self):
        return f'FAILURE: Expected {self.actual} {self.operator} {self.expected}'


class StepValidationException(Exception):
    pass

