from jasper import Feature
from unittest import TestCase


class FeatureTestCase(TestCase):

    def setUp(self):
        class MockScenario(object):

            def __init__(self):
                self.ran = False

            def run(self):
                self.ran = True

        self.scenarios = [MockScenario() for _ in range(5)]
        self.feature = Feature('Some_feature', *self.scenarios)

    def test_run(self):
        self.feature.run()

        for scenario in self.scenarios:
            self.assertTrue(scenario.ran)
