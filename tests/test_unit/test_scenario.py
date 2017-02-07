from jasper import Scenario, Given, When, Then, Context
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

            @staticmethod
            def cls(foo):
                return GivenMock(foo)

            @staticmethod
            def function():
                return 'foo'

        class WhenMock(When):

            def __init__(self, whatever):
                self.called = False
                self.called_with = None

            def __call__(self, context):
                self.called = True
                self.called_with = context

            def __str__(self):
                return 'When mock'

            @staticmethod
            def cls(foo):
                return WhenMock(foo)

            @staticmethod
            def function():
                return 'foo'

        class ThenMock(Then):

            def __init__(self, whatever):
                self.called = False
                self.called_with = None

            def __call__(self, context):
                self.called = True
                self.called_with = context

            def __str__(self):
                return 'Then mock'

            @staticmethod
            def cls(foo):
                return ThenMock(foo)

            @staticmethod
            def function():
                return 'foo'

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
        self.scenario.context = Context()
        self.scenario.run()

        self.assertTrue(self.scenario.given.called)
        self.assertEqual(self.scenario.given.called_with, self.scenario.context)

        self.assertTrue(self.scenario.when.called)
        self.assertEqual(self.scenario.when.called_with, self.scenario.context)

        self.assertTrue(self.scenario.then.called)
        self.assertEqual(self.scenario.then.called_with, self.scenario.context)
