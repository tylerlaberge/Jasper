from jasper import Suite, Feature, Scenario, given, when, then, Expect
from unittest import TestCase


class TestFeatureArithmetic(TestCase):
    def setUp(self):
        @given
        def an_adding_function(context):
            context.function = lambda a, b: a + b
            context.called_given = True

        @given
        def a_multiplication_function(context):
            context.function = lambda a, b: a * b
            context.called_given = True

        @when
        def we_call_it_with_two_negative_numbers(context):
            return {
                'called_when': True,
                'return_val': context.function(-5, -5)
            }

        @when
        def we_call_it_with_two_positive_numbers(context):
            return {
                'called_when': True,
                'return_val': context.function(5, 5)
            }

        @then
        def we_will_get_a_negative_number(context):
            context.result['called_then'] = True
            Expect(context.result['return_val']).to_be.less_than(0)

        @then
        def we_will_get_a_positive_number(context):
            context.result['called_then'] = True
            Expect(context.result['return_val']).to_be.greater_than(0)

        self.adding_two_negative_numbers_scenario = Scenario(
            'Adding two negative numbers',
            given=an_adding_function,
            when=we_call_it_with_two_negative_numbers,
            then=we_will_get_a_negative_number
        )
        self.adding_two_positive_numbers_scenario = Scenario(
            'Adding two positive numbers',
            given=an_adding_function,
            when=we_call_it_with_two_positive_numbers,
            then=we_will_get_a_positive_number
        )
        self.multiplying_two_negative_numbers_scenario = Scenario(
            'Multiplying two negative numbers',
            given=a_multiplication_function,
            when=we_call_it_with_two_negative_numbers,
            then=we_will_get_a_positive_number
        )
        self.multiplying_two_positive_numbers_scenario = Scenario(
            'Multiplying two positive numbers',
            given=a_multiplication_function,
            when=we_call_it_with_two_positive_numbers,
            then=we_will_get_a_positive_number
        )
        self.feature_one = Feature(
            'Addition',
            self.adding_two_negative_numbers_scenario,
            self.adding_two_positive_numbers_scenario
        )
        self.feature_two = Feature(
            'Multiplication',
            self.multiplying_two_negative_numbers_scenario,
            self.multiplying_two_positive_numbers_scenario
        )
        self.suite = Suite()
        self.suite.add_feature(self.feature_one)
        self.suite.add_feature(self.feature_two)

    def test_run(self):
        self.suite.run()

        for feature in self.suite.features:
            for scenario in feature.scenarios:
                self.assertTrue(scenario.context.called_given)
                self.assertTrue(scenario.context.result['called_when'])
                self.assertTrue(scenario.context.result['called_then'])
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
