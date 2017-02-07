import jasper
from unittest import TestCase


class GivenTestCase(TestCase):

    def setUp(self):

        @jasper.given
        def an_adding_function(context):
            context.function = lambda a, b: a + b

        self.given = an_adding_function.cls(an_adding_function.function)

    def test_initialize(self):
        self.assertEqual(type(self.given), jasper.Given)

    def test_call(self):
        context = jasper.Context()
        self.given(context)

        self.assertIn('function', context._items)

        result = context.function(63, 42)

        self.assertEqual(105, result)
