from jasper import Suite, Feature, Scenario, JasperGiven, JasperWhen, JasperThen, Expect
from unittest import TestCase


class TestFeatureArithmetic(TestCase):

    def setUp(self):

        class Given(JasperGiven):
            def an_adding_function(self):
                self.context.function = lambda a, b: a + b

            def a_multiplication_function(self):
                self.context.function = lambda a, b: a * b

        class When(JasperWhen):
            def we_call_it_with_two_negative_numbers(self):
                self.context.result = self.context.function(-5, -5)

            def we_call_it_with_two_positive_numbers(self):
                self.context.result = self.context.function(5, 5)

        class Then(JasperThen):
            def we_will_get_a_negative_number(self):
                Expect(self.context.result).to_be.less_than(0)

            def we_will_get_a_positive_number(self):
                Expect(self.context.result).to_be.greater_than(0)

        self.feature_one = Feature(
            'Arithmetic',
            Scenario(
                'Adding two negative numbers',
                Given('an_adding_function'),
                When('we_call_it_with_two_negative_numbers'),
                Then('we_will_get_a_negative_number')
            ),
            Scenario(
                'Adding two positive numbers',
                Given('an_adding_function'),
                When('we_call_it_with_two_positive_numbers'),
                Then('we_will_get_a_positive_number')
            ),
            Scenario(
                'Multiplying two positive numbers',
                Given('a_multiplication_function'),
                When('we_call_it_with_two_positive_numbers'),
                Then('we_will_get_a_positive_number')
            ),
            Scenario(
                'Multiplying two negative numbers',
                Given('a_multiplication_function'),
                When('we_call_it_with_two_negative_numbers'),
                Then('we_will_get_a_positive_number')
            )
        )
        self.feature_two = Feature(
            'Arithmetic Two',
            Scenario(
                'Adding two negative numbers',
                Given('an_adding_function'),
                When('we_call_it_with_two_negative_numbers'),
                Then('we_will_get_a_negative_number')
            ),
            Scenario(
                'Adding two positive numbers',
                Given('an_adding_function'),
                When('we_call_it_with_two_positive_numbers'),
                Then('we_will_get_a_positive_number')
            )
        )
        self.suite = Suite(self.feature_one, self.feature_two)

    def test_run(self):
        self.suite.run()

        self.assertTrue(self.suite.passed)
        self.assertEqual(self.suite.successes, [self.feature_one, self.feature_two])
        self.assertEqual(self.suite.failures, [])
        self.assertEqual(self.suite.num_features_passed, 2)
        self.assertEqual(self.suite.num_features_failed, 0)
        self.assertEqual(self.suite.num_scenarios_passed, 6)
        self.assertEqual(self.suite.num_scenarios_failed, 0)