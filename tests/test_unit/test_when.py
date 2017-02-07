import jasper
from unittest import TestCase


class WhenTestCase(TestCase):

    def setUp(self):

        @jasper.when
        def we_call_it_with_two_negative_numbers(context):
            return context.function(-5, -5)

        self.when = we_call_it_with_two_negative_numbers.cls(we_call_it_with_two_negative_numbers.function)

    def test_initialize(self):
        self.assertEqual(type(self.when), jasper.When)

    def test_call(self):
        context = jasper.Context(function=lambda a, b: a*b)
        self.when(context)

        self.assertIn('result', context._items)
        self.assertEqual(context.result, 25)
