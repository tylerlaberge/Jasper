from jasper import Feature
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

    def test_num_scenarios_passed(self):
        self.feature.successes = ['foo', 'bar']

        self.assertEqual(self.feature.num_scenarios_passed, 2)

    def test_num_scenarios_failed(self):
        self.feature.failures = ['foo', 'bar']

        self.assertEqual(self.feature.num_scenarios_failed, 2)
