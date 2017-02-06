import jasper
from jasper.exceptions import ExpectationException, ThenException
from unittest import TestCase


class ThenTestCase(TestCase):

    def setUp(self):

        @jasper.then
        def we_will_get_a_negative_number(context):
            if not context['result'] < 0:
                raise ExpectationException(context['result'], 0, 'to be less than')

        self.then = we_will_get_a_negative_number.cls(we_will_get_a_negative_number.function)

    def test_initialize(self):
        self.assertEqual(type(self.then), jasper.Then)

    def test_call_success(self):
        context = dict(result=-5)

        self.assertFalse(self.then.passed)

        self.then(context)

        self.assertTrue(self.then.passed)

    def test_call_failure(self):
        context = dict(result=5)

        with self.assertRaises(ThenException):
            self.then(context)

        self.assertFalse(self.then.passed)
