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
        self.operator = None

    def __call__(self, expected_data):
        """
        Make an assertion on based on the current operator.

        :param expected_data: The expected data to make assertions against the actual data with.
        :return: This Expect object.
        :raise ExpectationException: If the expectation fails.
        """
        if self.operator == 'to_be':
            if self.negate and self.actual_data is expected_data:
                raise ExpectationException(self.actual_data, expected_data, 'not_to_be')
            elif not self.negate and self.actual_data is not expected_data:
                raise ExpectationException(self.actual_data, expected_data, 'to_be')

        elif self.operator == 'to_equal':
            if self.negate and self.actual_data == expected_data:
                raise ExpectationException(self.actual_data, expected_data, 'not_to_equal')
            elif not self.negate and self.actual_data != expected_data:
                raise ExpectationException(self.actual_data, expected_data, 'to_equal')

        return self

    @property
    def not_(self):
        """
        Negate any operator that is set.

        :return: This Expect object.
        """
        self.negate = True
        return self

    @property
    def to_be(self):
        """
        Set the operator of this Expect object to the identity operator.

        Can also be used to chain into the less_than or greater_than assertions.

        :return: This Expect object.
        """
        self.operator = 'to_be'
        return self

    @property
    def to_equal(self):
        """
        Set the operator of this Expect object to the equality operator.

        :return: This Expect object.
        """
        self.operator = 'to_equal'
        return self

    def less_than(self, expected_data):
        """
        Make an assertion that this objects actual data is less than the expected data.

        The to_be operator must be set in order to use this assertion.

        :param expected_data: The data to expect the actual data to be less than.
        :return: This Expect object.
        :raise ExpectationException: If the expectation fails.
        """
        if self.operator == 'to_be':
            if self.negate and self.actual_data < expected_data:
                raise ExpectationException(self.actual_data, expected_data, 'not_to_be_less_than')
            elif not self.negate and not self.actual_data < expected_data:
                raise ExpectationException(self.actual_data, expected_data, 'to_be_less_than')

        return self

    def greater_than(self, expected_data):
        """
        Make an assertion that this objects actual data is greater than the expected data.

        The to_be operator must be set in order to use this assertion.

        :param expected_data: The data to expect the actual data to be less than.
        :return: This Expect object.
        :raise ExpectationException: If the expectation fails.
        """
        if self.operator == 'to_be':
            if self.negate and self.actual_data > expected_data:
                raise ExpectationException(self.actual_data, expected_data, 'not_to_be_greater_than')
            elif not self.negate and not self.actual_data > expected_data:
                raise ExpectationException(self.actual_data, expected_data, 'to_be_greater_than')

        return self
