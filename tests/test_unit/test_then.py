import jasper
from jasper.exceptions import ExpectationException
from unittest import TestCase
import asyncio


class ThenTestCase(TestCase):

    def setUp(self):

        @jasper.then
        def we_will_get_a_negative_number(context):
            if not context.result < 0:
                raise ExpectationException(context.result, 0, 'to be less than')

        self.then = we_will_get_a_negative_number()

    def test_initialize(self):
        self.assertEqual(type(self.then), jasper.Step)
        self.assertEqual(self.then.step_type, 'Then')

    def test_call_success(self):
        context = jasper.Context(result=-5)

        self.assertFalse(self.then.passed)

        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.then.run(context))

        self.assertTrue(self.then.passed)

    def test_call_failure(self):
        context = jasper.Context(result=5)
        loop = asyncio.get_event_loop()
        with self.assertRaises(ExpectationException):
            loop.run_until_complete(self.then.run(context))

        self.assertFalse(self.then.passed)
