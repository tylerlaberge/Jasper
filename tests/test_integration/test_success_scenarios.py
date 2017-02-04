from jasper import Scenario, JasperGiven, JasperWhen, JasperThen, Expect, Context
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

        self.scenarios = [
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
                'Multiplying two negative numbers',
                Given('a_multiplication_function'),
                When('we_call_it_with_two_negative_numbers'),
                Then('we_will_get_a_positive_number')
            ),
            Scenario(
                'Multiplying two positive numbers',
                Given('a_multiplication_function'),
                When('we_call_it_with_two_positive_numbers'),
                Then('we_will_get_a_positive_number')
            )
        ]

    def test_run(self):
        for scenario in self.scenarios:
            scenario.context = Context()
            scenario.run()

            self.assertTrue(scenario.passed)
