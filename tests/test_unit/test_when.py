import jasper
from unittest import TestCase
import asyncio


class WhenTestCase(TestCase):

    def setUp(self):

        @jasper.when
        def we_call_it_with_two_negative_numbers(context):
            context.result = context.function(-5, -5)

        self.when = we_call_it_with_two_negative_numbers()

    def test_initialize(self):
        self.assertEqual(type(self.when), jasper.When)

    def test_call(self):
        context = jasper.Context(function=lambda a, b: a*b)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.when.run(context))

        self.assertIn('result', context._items)
        self.assertEqual(context.result, 25)
