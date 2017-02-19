from jasper import Feature
from unittest import TestCase
import asyncio


class FeatureTestCase(TestCase):

    def setUp(self):
        class MockScenario(object):

            def __init__(self):
                self.passed = False

            def __str__(self):
                return 'foobar'

            async def run(self, context):
                self.passed = True

        self.scenarios = [MockScenario() for _ in range(5)]
        self.feature = Feature('Some_feature', scenarios=self.scenarios)

    def test_run(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.feature.run())

        for scenario in self.scenarios:
            self.assertTrue(scenario.passed)

        self.assertTrue(self.feature.passed)
        self.assertEqual(len(self.feature.successes), len(self.scenarios))
        self.assertEqual(self.feature.failures, [])

    def test_num_scenarios_passed(self):
        self.feature.successes = ['foo', 'bar']

        self.assertEqual(self.feature.num_scenarios_passed, 2)

    def test_num_scenarios_failed(self):
        self.feature.failures = ['foo', 'bar']

        self.assertEqual(self.feature.num_scenarios_failed, 2)
