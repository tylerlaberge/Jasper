import traceback


class ExpectationException(Exception):

    def __init__(self, actual, expected, operator):
        super()

        self.actual = actual
        self.expected = expected
        self.operator = operator
        self.msg = f'FAILURE: Expected {self.actual} {self.operator} {self.expected}'

    @property
    def relevant_trace(self):
        trace = traceback.format_tb(self.__traceback__)
        relevant_trace = trace[len(trace) - 2].split('\n')
        for index, line in enumerate(relevant_trace):
            relevant_trace[index] = line.strip()

        return relevant_trace
