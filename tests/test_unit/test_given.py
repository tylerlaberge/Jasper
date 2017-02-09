import jasper
from unittest import TestCase
import asyncio


class GivenTestCase(TestCase):

    def setUp(self):

        @jasper.given
        def an_adding_function(context):
            context.function = lambda a, b: a + b

        self.given_an_adding_function_one = an_adding_function()
        self.given_an_adding_function_two = an_adding_function()

    def test_initialize(self):
        self.assertEqual(type(self.given_an_adding_function_one), jasper.Given)
        self.assertEqual(type(self.given_an_adding_function_two), jasper.Given)

        self.assertNotEqual(id(self.given_an_adding_function_one), id(self.given_an_adding_function_two))

    def test_call(self):
        context_one = jasper.Context()

        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.given_an_adding_function_one.run(context_one))

        self.assertIn('function', context_one._items)
        self.assertEqual(105, context_one.function(63, 42))
