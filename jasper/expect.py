from jasper.exceptions import ExpectationException


class Expect(object):

    def __init__(self, actual_data):
        self.actual_data = actual_data

    @property
    def to_be(self):
        class ToBe(object):
            def __init__(self, actual_data):
                self.actual_data = actual_data

            def __call__(self, expected_data):
                if self.actual_data is not expected_data:
                    raise ExpectationException(self.actual_data, expected_data, 'to_be')

            def less_than(self, expected_data):
                if not self.actual_data < expected_data:
                    raise ExpectationException(self.actual_data, expected_data, 'to_be_less_than')

            def greater_than(self, expected_data):
                if not self.actual_data > expected_data:
                    raise ExpectationException(self.actual_data, expected_data, 'to_be_greater_than')

        return ToBe(self.actual_data)
