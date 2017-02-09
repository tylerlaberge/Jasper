import jasper
from unittest import TestCase
import asyncio


class GivenTestCase(TestCase):

    def setUp(self):

        @jasper.given
        def an_adding_function(context):
            context.function = lambda a, b: a + b

        @jasper.given
        def a_multiplication_function(context):
            context.function = lambda a, b: a * b

        self.given_an_adding_function = an_adding_function
        self.given_a_multiplication_function = a_multiplication_function

    def test_initialize(self):
        self.assertEqual(type(self.given_an_adding_function), jasper.Given)
        self.assertEqual(type(self.given_a_multiplication_function), jasper.Given)

        self.assertNotEqual(id(self.given_an_adding_function), id(self.given_a_multiplication_function))

    def test_call(self):
        context_one = jasper.Context()
        context_two = jasper.Context()

        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.given_an_adding_function(context_one))
        loop.run_until_complete(self.given_a_multiplication_function(context_two))

        self.assertIn('function', context_one._items)
        self.assertEqual(105, context_one.function(63, 42))

        self.assertIn('function', context_two._items)
        self.assertEqual(12, context_two.function(6, 2))
