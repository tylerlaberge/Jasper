import traceback
from jasper.utility import indent


class JasperException(Exception):

    @property
    def relevant_trace(self):
        trace = traceback.format_tb(self.__traceback__)
        relevant_trace = trace[len(trace) - 2].split('\n')
        for index, line in enumerate(relevant_trace):
            relevant_trace[index] = line.strip()

        return relevant_trace


class ExpectationException(JasperException):

    def __init__(self, actual, expected, operator):
        super()

        self.actual = actual
        self.expected = expected
        self.operator = operator
        self.msg = f'FAILURE: Expected {self.actual} {self.operator} {self.expected}'


class GivenException(JasperException):
    pass


class WhenException(JasperException):
    pass


class ThenException(JasperException):

    def __init__(self, original_exception):
        super()
        self.original_exception = original_exception

    def __str__(self):
        exception_string = f'{self.original_exception.msg}\n'
        trace_location_string = f'{self.original_exception.relevant_trace[0]}\n'
        trace_code_string = indent(f'{self.original_exception.relevant_trace[1]}\n', 4)

        return exception_string + trace_location_string + trace_code_string
