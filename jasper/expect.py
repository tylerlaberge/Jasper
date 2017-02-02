class Expect(object):

    def __init__(self, actual_data):
        self.actual_data = actual_data

    @property
    def to_be(self):
        class ToBe(object):
            def __init__(self, actual_data):
                self.actual_data = actual_data

            def __call__(self, expected_data):
                assert self.actual_data is expected_data

            def less_than(self, expected_data):
                assert self.actual_data < expected_data

            def greater_than(self, expected_data):
                assert self.actual_data > expected_data

        return ToBe(self.actual_data)