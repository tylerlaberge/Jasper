import jasper
from unittest import TestCase


class GivenTestCase(TestCase):

    def setUp(self):

        class Given(jasper.JasperGiven):

            def an_adding_function(self):
                self.context.function = lambda a, b: a + b

            def a_multiplication_function(self):
                self.context.function = lambda a, b: a * b

        self.given = Given

    def test_initialize(self):
        given_an_adding_function = self.given('an_adding_function')

        self.assertEqual(given_an_adding_function.given_function.__func__, self.given.an_adding_function)
        self.assertDictEqual(given_an_adding_function.context, {})
        self.assertFalse(given_an_adding_function.passed)

    def test_call(self):
        context = jasper.Context({})
        given_an_adding_function = self.given('an_adding_function')
        given_an_adding_function(context)

        self.assertIn('function', given_an_adding_function.context)

        result = given_an_adding_function.context.function(63, 42)

        self.assertEqual(105, result)
