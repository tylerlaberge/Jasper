from jasper import Scenario, Given, When, Then, Context
from unittest import TestCase
import asyncio


class ScenarioTestCase(TestCase):

    def setUp(self):

        run_order = []

        class GivenMock(Given):

            def __init__(self, whatever):
                self.called = False
                self.called_with = None

            async def run(self, context):
                self.called = True
                self.called_with = context
                run_order.append(self)

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

            async def run(self, context):
                self.called = True
                self.called_with = context
                run_order.append(self)

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

            async def run(self, context):
                self.called = True
                self.called_with = context
                run_order.append(self)

            def __str__(self):
                return 'Then mock'

            @staticmethod
            def cls(foo):
                return ThenMock(foo)

            @staticmethod
            def function():
                return 'foo'

        self.given_mock = GivenMock
        self.when_mock = WhenMock
        self.then_mock = ThenMock
        self.run_order = run_order
        self.scenario = Scenario(
            'pre_made_scenario',
            given=self.given_mock('foo'),
            when=self.when_mock('foo'),
            then=self.then_mock('foo')
        )

    def test_call(self):
        self.scenario('foobar')

        self.assertEqual(self.scenario.context, 'foobar')

    def test_run_single_steps(self):
        given_mock = self.given_mock('foo')
        when_mock = self.when_mock('foo')
        then_mock = self.then_mock('foo')
        scenario = Scenario(
            'single_steps_scenario',
            given=given_mock,
            when=when_mock,
            then=then_mock
        )
        scenario.context = Context()
        loop = asyncio.get_event_loop()
        loop.run_until_complete(scenario.run())

        self.assertTrue(given_mock.called)
        self.assertEqual(given_mock.called_with, scenario.context)

        self.assertTrue(when_mock.called)
        self.assertEqual(when_mock.called_with, scenario.context)

        self.assertTrue(then_mock.called)
        self.assertEqual(then_mock.called_with, scenario.context)

        self.assertEqual(self.run_order, [given_mock, when_mock, then_mock])

    def test_run_multiple_steps(self):
        given_mock_one = self.given_mock('foo')
        given_mock_two = self.given_mock('foo')
        when_mock_one = self.when_mock('foo')
        when_mock_two = self.when_mock('foo')
        then_mock_one = self.then_mock('foo')
        then_mock_two = self.then_mock('foo')
        scenario = Scenario(
            'multiple_steps_scenario',
            given=[given_mock_one, given_mock_two],
            when=[when_mock_one, when_mock_two],
            then=[then_mock_one, then_mock_two]
        )
        scenario.context = Context()
        loop = asyncio.get_event_loop()
        loop.run_until_complete(scenario.run())

        self.assertTrue(given_mock_one.called)
        self.assertTrue(given_mock_two.called)
        self.assertEqual(given_mock_one.called_with, scenario.context)
        self.assertEqual(given_mock_two.called_with, scenario.context)

        self.assertTrue(when_mock_one.called)
        self.assertTrue(when_mock_two.called)
        self.assertEqual(when_mock_one.called_with, scenario.context)
        self.assertEqual(when_mock_two.called_with, scenario.context)

        self.assertTrue(then_mock_one.called)
        self.assertTrue(then_mock_two.called)
        self.assertEqual(then_mock_one.called_with, scenario.context)
        self.assertEqual(then_mock_two.called_with, scenario.context)

        self.assertEqual(self.run_order, [
            given_mock_one, given_mock_two,
            when_mock_one, when_mock_two,
            then_mock_one, then_mock_two
        ])
