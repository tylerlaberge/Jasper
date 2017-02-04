from jasper.utility import extract_traceback


class JasperException(Exception):
    pass


class ExpectationException(JasperException):

    def __init__(self, actual, expected, operator):
        super()
        self.actual = actual
        self.expected = expected
        self.operator = operator

    def __str__(self):
        return f'Expected {self.actual} {self.operator} {self.expected}'


class JasperClauseException(JasperException):

    def __init__(self, original_exception):
        self.original_exception = original_exception
        super()

    def __str__(self):
        if str(self.original_exception):
            exception_string = f'{str(self.original_exception)}\n\n'
        else:
            exception_string = f'{self.original_exception.__class__.__name__}\n\n'

        traceback_string = f'{self.get_traceback()}'

        return exception_string + traceback_string

    def get_traceback(self):
        return extract_traceback(self.original_exception)


class GivenException(JasperClauseException):
    pass


class WhenException(JasperClauseException):
    pass


class ThenException(JasperClauseException):
    pass

