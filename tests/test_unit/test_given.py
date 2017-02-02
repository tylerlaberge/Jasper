import jasper
from unittest import TestCase


class GivenTestCase(TestCase):

    def setUp(self):

        class Given(jasper.JasperGiven):

            def an_adding_function(self, a, b):
                return a + b

            def a_multiplication_function(self, a, b):
                return a * b

        self.given = Given

    def test_initialize(self):
        given_an_adding_function = self.given('an_adding_function')

        self.assertDictEqual(
            given_an_adding_function.context,
            {'an_adding_function': given_an_adding_function.an_adding_function}
        )

    def test_initialize_with_alias(self):
        given_a_multiplication_function = self.given('a_multiplication_function', with_alias='function')

        self.assertDictEqual(
            given_a_multiplication_function.context,
            {'function': given_a_multiplication_function.a_multiplication_function}
        )

    def test_call(self):
        context = jasper.Context({})
        given_an_adding_function = self.given('an_adding_function')
        given_an_adding_function(context)

        self.assertDictEqual(context, {'an_adding_function': given_an_adding_function.an_adding_function})
