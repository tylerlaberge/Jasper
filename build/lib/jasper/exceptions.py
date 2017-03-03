"""
The exceptions module.
"""


class ExpectationException(Exception):
    """
    An Exception that is thrown when an expectation fails in the Expect class.
    """
    def __init__(self, actual, expected, operator):
        """
        Initialize this ExpectationException object.

        :param actual: The actual data used during the expectation.
        :param expected: The expected data used during the expectation.
        :param operator: The operator used during the expectation.
        """
        super().__init__()
        self.actual = actual
        self.expected = expected
        self.operator = operator

    def __str__(self):
        return f'FAILURE: Expected {self.actual} {self.operator} {self.expected}'


class ValidationException(Exception):
    """
    An Exception that is thrown when an object fails validation during construction.
    """
    pass

