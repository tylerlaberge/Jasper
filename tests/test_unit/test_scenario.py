from jasper import Scenario
from unittest import TestCase


class ScenarioTestCase(TestCase):

    def setUp(self):
        class Mock(object):

            def __init__(self, whatever):
                self.called = False
                self.called_with = None

            def __call__(self, context):
                self.called = True
                self.called_with = context

        self.given_mock = Mock('given')
        self.when_mock = Mock('when')
        self.then_mock = Mock('then')

        self.scenario = Scenario(
            'mock_scenario',
            given=self.given_mock,
            when=self.when_mock,
            then=self.then_mock
        )

    def test_call(self):
        self.scenario('foobar')

        self.assertEqual(self.scenario.context, 'foobar')

    def test_run(self):
        self.scenario.context = {}
        self.scenario.run()

        self.assertTrue(self.given_mock.called)
        self.assertEqual(self.given_mock.called_with, self.scenario.context)

        self.assertTrue(self.when_mock.called)
        self.assertEqual(self.when_mock.called_with, self.scenario.context)

        self.assertTrue(self.then_mock.called)
        self.assertEqual(self.then_mock.called_with, self.scenario.context)