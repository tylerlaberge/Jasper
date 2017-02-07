from jasper import Suite
from unittest import TestCase
import asyncio


class SuiteTestCase(TestCase):

    def setUp(self):
        self.maxDiff = None

        class MockFeatureSuccess(object):

            def __init__(self):
                self.passed = False

            def __str__(self):
                return 'foobar\n'

            async def run(self):
                self.passed = True

            @property
            def num_scenarios_passed(self):
                return 5

            @property
            def num_scenarios_failed(self):
                return 3

        class MockFeatureFailure(object):
            def __init__(self):
                self.passed = False

            def __str__(self):
                return 'foobar\n'

            async def run(self):
                self.passed = False

            @property
            def num_scenarios_passed(self):
                return 5

            @property
            def num_scenarios_failed(self):
                return 3

        self.features = [MockFeatureSuccess(), MockFeatureFailure(), MockFeatureSuccess(), MockFeatureFailure()]
        self.suite = Suite()

        for feature in self.features:
            self.suite.add_feature(feature)

    def test_run(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.suite.run())

        self.assertEqual(len(self.suite.successes), 2)
        self.assertEqual(len(self.suite.failures), 2)

    def test_num_features_passed(self):
        self.suite.successes = ['foo', 'bar']

        self.assertEqual(self.suite.num_features_passed, 2)

    def test_num_features_failed(self):
        self.suite.failures = ['foo', 'bar']

        self.assertEqual(self.suite.num_features_failed, 2)

    def test_num_scenarios_passed(self):
        self.assertEqual(self.suite.num_scenarios_passed, 20)

    def test_num_scenarios_failed(self):
        self.assertEqual(self.suite.num_scenarios_failed, 12)
