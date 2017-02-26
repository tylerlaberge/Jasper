from unittest import TestCase
from jasper.exceptions import ExpectationException, ValidationException


class ExpectationExceptionTestCase(TestCase):

    def test_init(self):
        expectation_exception = ExpectationException('foo', 'bar', 'some_operator')

        self.assertTrue(isinstance(expectation_exception, Exception))
        self.assertEqual(expectation_exception.actual, 'foo')
        self.assertEqual(expectation_exception.expected, 'bar')
        self.assertEqual(expectation_exception.operator, 'some_operator')

    def test_str(self):
        expectation_exception = ExpectationException('foo', 'bar', 'some_operator')

        self.assertEqual(str(expectation_exception), 'FAILURE: Expected foo some_operator bar')

    def test_raise(self):
        with self.assertRaises(ExpectationException):
            raise ExpectationException('foo', 'bar', 'some_operator')


class ValidationExceptionTestCase(TestCase):

    def test_init(self):
        validation_exception = ValidationException()

        self.assertTrue(isinstance(validation_exception, Exception))

    def test_raise(self):
        with self.assertRaises(ValidationException):
            raise ValidationException()
