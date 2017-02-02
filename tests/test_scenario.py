from jasper import Scenario
from unittest import TestCase


class ScenarioTestCase(TestCase):

    def setUp(self):
        class Mock(object):

            def __init__(self, whatever):
                self.called = False

            def __call__(self, context):
                self.called = True

        self.given_mock = Mock('given')
        self.when_mock = Mock('when')
        self.then_mock = Mock('then')

        self.scenario = Scenario(
            given=self.given_mock,
            when=self.when_mock,
            then=self.then_mock
        )

    def test_prepare_given(self):

        self.scenario.prepare_given()

        self.assertTrue(self.given_mock.called)
        self.assertTrue(self.scenario.prepared_given)

    def test_run_when(self):
        self.scenario.prepared_given = True
        self.scenario.run_when()

        self.assertTrue(self.when_mock.called)
        self.assertTrue(self.scenario.ran_when)

    def test_run_then(self):
        self.scenario.ran_when = True
        self.scenario.run_then()

        self.assertTrue(self.then_mock.called)
        self.assertTrue(self.scenario.ran_then)

    def test_run_when_out_of_order(self):
        with self.assertRaises(ValueError):
            self.scenario.run_when()

        self.assertFalse(self.when_mock.called)
        self.assertFalse(self.scenario.ran_when)

    def test_run_then_out_of_order(self):
        with self.assertRaises(ValueError):
            self.scenario.run_then()

        self.assertFalse(self.then_mock.called)
        self.assertFalse(self.scenario.ran_then)
