from jasper.exceptions import ExpectationException


class Expect(object):

    def __init__(self, actual_data):
        self.actual_data = actual_data
        self.negate = False
        self.operator = None

    def __call__(self, expected_data):
        if self.operator == 'to_be':
            if self.negate and self.actual_data is expected_data:
                raise ExpectationException(self.actual_data, expected_data, 'not_to_be')
            elif not self.negate and self.actual_data is not expected_data:
                raise ExpectationException(self.actual_data, expected_data, 'to_be')

        return self

    @property
    def not_(self):
        self.negate = True
        return self

    @property
    def to_be(self):
        self.operator = 'to_be'
        return self

    def less_than(self, expected_data):
        if self.operator == 'to_be':
            if self.negate and self.actual_data < expected_data:
                raise ExpectationException(self.actual_data, expected_data, 'not_to_be_less_than')
            elif not self.negate and not self.actual_data < expected_data:
                raise ExpectationException(self.actual_data, expected_data, 'to_be_less_than')

        return self

    def greater_than(self, expected_data):
        if self.operator == 'to_be':
            if self.negate and self.actual_data > expected_data:
                raise ExpectationException(self.actual_data, expected_data, 'not_to_be_greater_than')
            elif not self.negate and not self.actual_data > expected_data:
                raise ExpectationException(self.actual_data, expected_data, 'to_be_greater_than')

        return self
