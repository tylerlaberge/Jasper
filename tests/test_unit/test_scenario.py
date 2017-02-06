from jasper import Scenario, Given, When, Then
from unittest import TestCase


class ScenarioTestCase(TestCase):

    def setUp(self):

        class GivenMock(Given):

            def __init__(self, whatever):
                self.called = False
                self.called_with = None

            def __call__(self, context):
                self.called = True
                self.called_with = context

            def __str__(self):
                return 'Given mock'

        class WhenMock(When):

            def __init__(self, whatever):
                self.called = False
                self.called_with = None

            def __call__(self, context):
                self.called = True
                self.called_with = context

            def __str__(self):
                return 'When mock'

        class ThenMock(Then):

            def __init__(self, whatever):
                self.called = False
                self.called_with = None

            def __call__(self, context):
                self.called = True
                self.called_with = context

            def __str__(self):
                return 'Then mock'

        self.given_mock = GivenMock('foo')
        self.when_mock = WhenMock('bar')
        self.then_mock = ThenMock('baz')

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