from unittest import TestCase
from jasper.suite import Suite
import asyncio


class SuiteTestCase(TestCase):

    def setUp(self):

        class PassingFeatureMock(object):

            def __init__(self):
                self.ran = False
                self.passed = False
                self.scenarios = ['foo', 'bar']

            async def run(self):
                self.ran = True
                self.passed = True

        class FailingFeatureMock(object):

            def __init__(self):
                self.ran = False
                self.passed = False
                self.scenarios = ['foobar', 'barfoo']

            async def run(self):
                self.ran = True
                self.passed = False

        self.passing_feature_mock = PassingFeatureMock
        self.failing_feature_mock = FailingFeatureMock
        self.loop = asyncio.new_event_loop()

    def tearDown(self):
        self.loop.close()

    def test_init(self):
        suite = Suite()

        self.assertEqual(suite.features, [])
        self.assertEqual(suite.successes, [])
        self.assertEqual(suite.failures, [])
        self.assertTrue(suite.passed)

    def test_add_feature(self):
        suite = Suite()

        feature_one = self.passing_feature_mock()
        feature_two = self.failing_feature_mock()

        suite.add_feature(feature_one)

        self.assertEqual(suite.features, [feature_one])

        suite.add_feature(feature_two)

        self.assertEqual(suite.features, [feature_one, feature_two])

    def test_successful_run(self):
        suite = Suite()

        feature_one = self.passing_feature_mock()
        feature_two = self.passing_feature_mock()

        suite.features = [feature_one, feature_two]

        self.loop.run_until_complete(suite.run())

        self.assertTrue(feature_one.ran)
        self.assertTrue(feature_two.ran)
        self.assertEqual(len(suite.successes), 2)
        self.assertTrue(feature_one in suite.successes)
        self.assertTrue(feature_two in suite.successes)
        self.assertEqual(suite.failures, [])
        self.assertTrue(suite.passed)

    def test_failure_run(self):
        suite = Suite()

        passing_feature = self.passing_feature_mock()
        failing_feature = self.failing_feature_mock()

        suite.features = [passing_feature, failing_feature]

        self.loop.run_until_complete(suite.run())

        self.assertTrue(passing_feature.ran)
        self.assertTrue(failing_feature.ran)
        self.assertEqual(suite.successes, [passing_feature])
        self.assertEqual(suite.failures, [failing_feature])
        self.assertFalse(suite.passed)
