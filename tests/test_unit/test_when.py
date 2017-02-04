import jasper
from unittest import TestCase


class WhenTestCase(TestCase):

    def setUp(self):

        class When(jasper.JasperWhen):
            def we_call_it_with_two_negative_numbers(self):
                self.context.result = self.context.function(-5, -5)

            def we_call_it_with_two_positive_numbers(self):
                self.context.result = self.context.function(5, 5)

        self.when = When

    def test_initialize(self):
        when_we_call_it_with_two_negative_numbers = self.when('we_call_it_with_two_negative_numbers')

        self.assertEqual(
            when_we_call_it_with_two_negative_numbers.when_function,
            when_we_call_it_with_two_negative_numbers.we_call_it_with_two_negative_numbers
        )

    def test_call(self):

        context = jasper.Context({'function': lambda a, b: a*b})
        when_we_call_it_with_two_positive_numbers = self.when('we_call_it_with_two_positive_numbers')
        when_we_call_it_with_two_positive_numbers(context)

        self.assertEqual(when_we_call_it_with_two_positive_numbers.context, context)
        self.assertEqual(when_we_call_it_with_two_positive_numbers.context.result, 25)
