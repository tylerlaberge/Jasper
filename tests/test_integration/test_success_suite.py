from jasper import Suite, Feature, Scenario, given, when, then, Expect
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

        self.adding_two_negative_numbers_scenario = Scenario(
            'Adding two negative numbers',
            given=an_adding_function(),
            when=we_call_it_with_two_negative_numbers(),
            then=we_will_get_a_negative_number()
        )
        self.adding_two_positive_numbers_scenario = Scenario(
            'Adding two positive numbers',
            given=an_adding_function(),
            when=we_call_it_with_two_positive_numbers(),
            then=we_will_get_a_positive_number()
        )
        self.multiplying_two_negative_numbers_scenario = Scenario(
            'Multiplying two negative numbers',
            given=a_multiplication_function(),
            when=we_call_it_with_two_negative_numbers(),
            then=we_will_get_a_positive_number()
        )
        self.multiplying_two_positive_numbers_scenario = Scenario(
            'Multiplying two positive numbers',
            given=a_multiplication_function(),
            when=we_call_it_with_two_positive_numbers(),
            then=we_will_get_a_positive_number()
        )
        self.feature_one = Feature(
            'Addition',
            scenarios=[
                self.adding_two_negative_numbers_scenario,
                self.adding_two_positive_numbers_scenario
            ]
        )
        self.feature_two = Feature(
            'Multiplication',
            scenarios=[
                self.multiplying_two_negative_numbers_scenario,
                self.multiplying_two_positive_numbers_scenario
            ]
        )
        self.suite = Suite()
        self.suite.add_feature(self.feature_one)
        self.suite.add_feature(self.feature_two)

    def test_run(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.suite.run())

        for feature in self.suite.features:
            for scenario in feature.scenarios:
                self.assertTrue(scenario.ran)
                self.assertIsNone(scenario.exception)
                self.assertTrue(scenario.passed)

            self.assertTrue(feature.passed)
            self.assertEqual(len(feature.successes), 2)
            self.assertEqual(len(feature.failures), 0)
            self.assertEqual(set(feature.failures), set())
            self.assertEqual(feature.num_scenarios_passed, 2)
            self.assertEqual(feature.num_scenarios_failed, 0)

        self.assertEqual(set(self.suite.features[0].successes), {
            self.adding_two_negative_numbers_scenario,
            self.adding_two_positive_numbers_scenario
        })
        self.assertEqual(set(self.suite.features[1].successes), {
            self.multiplying_two_negative_numbers_scenario,
            self.multiplying_two_positive_numbers_scenario
        })

        self.assertEqual(len(self.suite.successes), 2)
        self.assertEqual(set(self.suite.successes), {
            self.feature_one, self.feature_two
        })
        self.assertEqual(len(self.suite.failures), 0)
        self.assertEqual(set(self.suite.failures), set())
        self.assertTrue(self.suite.passed)
        self.assertEqual(self.suite.num_features_passed, 2)
        self.assertEqual(self.suite.num_features_failed, 0)
        self.assertEqual(self.suite.num_scenarios_passed, 4)
        self.assertEqual(self.suite.num_scenarios_failed, 0)
