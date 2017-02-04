from jasper import Suite
from jasper.utility import cyan, red
from unittest import TestCase


class SuiteTestCase(TestCase):

    def setUp(self):
        self.maxDiff = None

        class MockFeatureSuccess(object):

            def __init__(self):
                self.passed = False

            def __str__(self):
                return 'foobar\n'

            def run(self):
                self.passed = True

        class MockFeatureFailure(object):
            def __init__(self):
                self.passed = False

            def __str__(self):
                return 'foobar\n'

            def run(self):
                self.passed = False

        self.features = [MockFeatureSuccess(), MockFeatureFailure(), MockFeatureSuccess(), MockFeatureFailure()]
        self.suite = Suite(*self.features)

    def test_run(self):
        self.suite.run()

        self.assertEqual(self.suite.successes, [self.features[0], self.features[2]])
        self.assertEqual(self.suite.failures, [self.features[1], self.features[3]])

    def test_str(self):
        self.suite.run()

        expected_success_string = cyan('='*150) + '\n'
        expected_success_string += 'foobar\n'
        expected_success_string += cyan('='*150) + '\n'
        expected_success_string *= 2

        expected_faiure_string = red('=' * 150) + '\n'
        expected_faiure_string += 'foobar\n'
        expected_faiure_string += red('=' * 150) + '\n'
        expected_faiure_string *= 2

        expected_string = expected_success_string + expected_faiure_string

        self.assertEqual(str(self.suite), expected_string)
