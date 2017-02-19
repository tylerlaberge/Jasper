from jasper import Scenario, given, when, then, Expect, Context
from unittest import TestCase
import asyncio


class TestFeatureArithmetic(TestCase):

    def setUp(self):

        @given
        def an_adding_function(context):
            context.function = lambda a, b: a + b

        @given
        def a_multiplication_function(context):
            context.function = lambda a, b: a * b

        @when
        def we_call_it_with_two_negative_numbers(context):
            context.result = context.function(-5, -5)

        @when
        def we_call_it_with_two_positive_numbers(context):
            context.result = context.function(5, 5)

        @then
        def we_will_get_a_negative_number(context):
            Expect(context.result).to_be.less_than(0)

        @then
        def we_will_get_a_positive_number(context):
            Expect(context.result).to_be.greater_than(0)

        self.scenarios = [
            Scenario(
                'Adding two negative numbers',
                given=an_adding_function(),
                when=we_call_it_with_two_negative_numbers(),
                then=we_will_get_a_negative_number()
            ),
            Scenario(
                'Adding two positive numbers',
                given=an_adding_function(),
                when=we_call_it_with_two_positive_numbers(),
                then=we_will_get_a_positive_number()
            ),
            Scenario(
                'Multiplying two negative numbers',
                given=a_multiplication_function(),
                when=we_call_it_with_two_negative_numbers(),
                then=we_will_get_a_positive_number()
            ),
            Scenario(
                'Multiplying two positive numbers',
                given=a_multiplication_function(),
                when=we_call_it_with_two_positive_numbers(),
                then=we_will_get_a_positive_number()
            )
        ]

    def test_run(self):
        loop = asyncio.get_event_loop()
        for scenario in self.scenarios:
            scenario.context = Context()
            loop.run_until_complete(scenario.run(Context()))

            self.assertTrue(scenario.ran)
            self.assertIsNone(scenario.exception)
            self.assertTrue(scenario.passed)
