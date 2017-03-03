"""
The expect module.
"""

from jasper.exceptions import ExpectationException


class Expect(object):
    """
    A class for making assertions on data.
    """
    def __init__(self, actual_data):
        """
        Initialize a new Expect object.

        :param actual_data: The actual data to make assertions against.
        """
        self.actual_data = actual_data
        self.negate = False

    def not_(self):
        """
        Negate any future expectations.

        :return: This Expect object.
        """
        self.negate = True
        return self

    def to_be(self, expected_data):
        """
        Make an assertion that this objects actual data is the expected data.

        :param expected_data: The data to expect the actual data to be.
        :raise ExpectationException: If the expectation fails.
        """
        if self.negate and self.actual_data is expected_data:
            raise ExpectationException(self.actual_data, expected_data, 'not_to_be')
        elif not self.negate and self.actual_data is not expected_data:
            raise ExpectationException(self.actual_data, expected_data, 'to_be')

    def to_equal(self, expected_data):
        """
        Make an assertion that this objects actual data is equal to the expected data.

        :param expected_data: The data to expect the actual data to be equal to.
        :raise ExpectationException: If the expectation fails.
        """
        if self.negate and self.actual_data == expected_data:
            raise ExpectationException(self.actual_data, expected_data, 'not_to_equal')
        elif not self.negate and self.actual_data != expected_data:
            raise ExpectationException(self.actual_data, expected_data, 'to_equal')

    def to_be_less_than(self, expected_data):
        """
        Make an assertion that this objects actual data is less than the expected data.

        :param expected_data: The data to expect the actual data to be less than.
        :raise ExpectationException: If the expectation fails.
        """
        if self.negate and self.actual_data < expected_data:
            raise ExpectationException(self.actual_data, expected_data, 'not_to_be_less_than')
        elif not self.negate and not self.actual_data < expected_data:
            raise ExpectationException(self.actual_data, expected_data, 'to_be_less_than')

    def to_be_greater_than(self, expected_data):
        """
        Make an assertion that this objects actual data is greater than the expected data.

        :param expected_data: The data to expect the actual data to be less than.
        :raise ExpectationException: If the expectation fails.
        """
        if self.negate and self.actual_data > expected_data:
            raise ExpectationException(self.actual_data, expected_data, 'not_to_be_greater_than')
        elif not self.negate and not self.actual_data > expected_data:
            raise ExpectationException(self.actual_data, expected_data, 'to_be_greater_than')

    def to_be_less_than_or_equal_to(self, expected_data):
        """
        Make an assertion that this objects actual data is less than or equal to the expected data

        :param expected_data: The data to expect the actual data to be less than or equal to.
        :raise ExpectationException: If the expectation fails.
        """
        if self.negate and self.actual_data <= expected_data:
            raise ExpectationException(self.actual_data, expected_data, 'not_to_be_less_than_or_equal_to')
        elif not self.negate and not self.actual_data <= expected_data:
            raise ExpectationException(self.actual_data, expected_data, 'to_be_less_than_or_equal_to')

    def to_be_greater_than_or_equal_to(self, expected_data):
        """
        Make an assertion that this objects actual data is greater than or equal to the expected data

        :param expected_data: The data to expect the actual data to be greater than or equal to.
        :raise ExpectationException: If the expectation fails.
        """
        if self.negate and self.actual_data >= expected_data:
            raise ExpectationException(self.actual_data, expected_data, 'not_to_be_greater_than_or_equal_to')
        elif not self.negate and not self.actual_data >= expected_data:
            raise ExpectationException(self.actual_data, expected_data, 'to_be_greater_than_or_equal_to')