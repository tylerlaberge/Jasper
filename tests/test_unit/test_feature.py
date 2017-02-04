from jasper import Feature
from jasper.utility import cyan, indent
from unittest import TestCase


class FeatureTestCase(TestCase):

    def setUp(self):
        class MockScenario(object):

            def __init__(self):
                self.passed = False

            def __call__(self, context):
                self.context = context

            def __str__(self):
                return 'foobar'

            def run(self):
                self.passed = True

        self.scenarios = [MockScenario() for _ in range(5)]
        self.feature = Feature('Some_feature', *self.scenarios)

    def test_run(self):
        self.feature.run()

        for scenario in self.scenarios:
            self.assertTrue(scenario.passed)
            self.assertIsNotNone(scenario.context)

        self.assertTrue(self.feature.passed)
        self.assertEqual(self.feature.successes, self.scenarios)
        self.assertEqual(self.feature.failures, [])

    def test_str(self):
        self.feature.run()

        formatted_string = cyan(f'Feature: Some_feature\n')
        for scenario in self.scenarios:
            formatted_string += indent(f'{scenario}\n', 4)

        self.assertEqual(str(self.feature), formatted_string)