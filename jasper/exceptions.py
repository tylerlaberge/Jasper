class ExpectationException(Exception):

    def __init__(self, actual, expected, operator):
        super()

        self.actual = actual
        self.expected = expected
        self.operator = operator
        self.msg = f'Expected {self.actual} {self.operator} {self.expected}'
