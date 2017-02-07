import jasper
from jasper.exceptions import ExpectationException, ThenException
from unittest import TestCase
import asyncio


class ThenTestCase(TestCase):

    def setUp(self):

        @jasper.then
        def we_will_get_a_negative_number(context):
            if not context.result < 0:
                raise ExpectationException(context['result'], 0, 'to be less than')

        self.then = we_will_get_a_negative_number.cls(we_will_get_a_negative_number.function)

    def test_initialize(self):
        self.assertEqual(type(self.then), jasper.Then)

    def test_call_success(self):
        context = jasper.Context(result=-5)

        self.assertFalse(self.then.passed)

        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.then(context))

        self.assertTrue(self.then.passed)

    def test_call_failure(self):
        context = jasper.Context(result=5)
        loop = asyncio.get_event_loop()
        with self.assertRaises(ThenException):
            loop.run_until_complete(self.then(context))

        self.assertFalse(self.then.passed)
