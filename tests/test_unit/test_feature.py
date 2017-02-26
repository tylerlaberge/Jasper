from unittest import TestCase
from unittest.mock import MagicMock, patch
from jasper.feature import Feature
from jasper.scenario import Scenario
from jasper.step import Step
import asyncio


class ScenarioTestCase(TestCase):

    def setUp(self):
        call_order = []
        mock_step = MagicMock(spec=Step)
        mock_scenario = MagicMock(spec=Scenario)

        class StepMock(mock_step.__class__):

            def __init__(self):
                self.run_called = False
                self.run_called_with = None
                self.run_call_count = 0
                self.passed = False

            async def run(self, context):
                self.run_called = True
                self.run_called_with = context
                self.run_call_count += 1
                self.passed = True
                call_order.append(self)

        class ScenarioMock(mock_scenario.__class__):

            def __init__(self):
                self.run_called = False
                self.run_called_with = None
                self.run_call_count = 0
                self.passed = False

            async def run(self, context):
                self.run_called = True
                self.run_called_with = context
                self.run_call_count += 1
                self.passed = True

        self.call_order = call_order

        self.scenario_mock_one = ScenarioMock()
        self.scenario_mock_two = ScenarioMock()
        self.before_all_mock = StepMock()
        self.after_all_mock = StepMock()
        self.before_each_mock = StepMock()
        self.after_each_mock = StepMock()
        self.loop = asyncio.new_event_loop()

    def tearDown(self):
        self.loop.close()

    def test_init(self):
        feature = Feature('foobar',
                          scenarios=[self.scenario_mock_one, self.scenario_mock_two],
                          before_all=self.before_all_mock, after_all=self.after_all_mock,
                          before_each=self.before_each_mock, after_each=self.after_each_mock)

        self.assertEqual(feature.description, 'foobar')
        self.assertEqual(feature.scenarios, [self.scenario_mock_one, self.scenario_mock_two])
        self.assertEqual(feature.before_each, [self.before_each_mock])
        self.assertEqual(feature.before_all, [self.before_all_mock])
        self.assertEqual(feature.after_each, [self.after_each_mock])
        self.assertEqual(feature.after_all, [self.after_all_mock])
        self.assertIsNone(feature.exception)
        self.assertTrue(feature.passed)
        self.assertEqual(feature.successes, [])
        self.assertEqual(feature.failures, [])

    @patch('jasper.feature.Context')
    def test_successful_run(self, mock_context):
        feature = Feature('foobar',
                          scenarios=[self.scenario_mock_one, self.scenario_mock_two],
                          before_all=self.before_all_mock, after_all=self.after_all_mock,
                          before_each=self.before_each_mock, after_each=self.after_each_mock)

        try:
            self.loop.run_until_complete(feature.run())
        except Exception:
            raise AssertionError
        else:
            def assert_mock_called_correctly(mock, call_count):
                self.assertTrue(mock.run_called)
                self.assertTrue(isinstance(mock.run_called_with, MagicMock))
                self.assertEqual(mock.run_call_count, call_count)

            assert_mock_called_correctly(self.before_all_mock, 1)
            assert_mock_called_correctly(self.before_each_mock, 2)
            assert_mock_called_correctly(self.after_each_mock, 2)
            assert_mock_called_correctly(self.after_all_mock, 1)

            assert_mock_called_correctly(self.scenario_mock_one, 1)
            assert_mock_called_correctly(self.scenario_mock_two, 1)

            self.assertEqual(self.call_order, [
                self.before_all_mock,
                self.before_each_mock, self.after_each_mock,
                self.before_each_mock, self.after_each_mock,
                self.after_all_mock
            ])

            self.assertEqual(len(feature.successes), 2)
            self.assertTrue(self.scenario_mock_one in feature.successes)
            self.assertTrue(self.scenario_mock_two in feature.successes)
            self.assertEqual(feature.failures, [])
            self.assertTrue(feature.passed)

    @patch('jasper.feature.Context')
    def test_failure_run(self, mock_context):
        mock_scenario = MagicMock(spec=Scenario)

        class ScenarioFailureMock(mock_scenario.__class__):

            def __init__(self):
                self.run_called = False
                self.run_called_with = None
                self.run_call_count = 0
                self.passed = False

            async def run(self, context):
                self.run_called = True
                self.run_called_with = context
                self.run_call_count += 1
                self.passed = False

        failure_scenario = ScenarioFailureMock()

        feature = Feature('foobar',
                          scenarios=[self.scenario_mock_one, failure_scenario],
                          before_all=self.before_all_mock, after_all=self.after_all_mock,
                          before_each=self.before_each_mock, after_each=self.after_each_mock)

        try:
            self.loop.run_until_complete(feature.run())
        except Exception:
            raise AssertionError
        else:
            def assert_mock_called_correctly(mock, call_count):
                self.assertTrue(mock.run_called)
                self.assertTrue(isinstance(mock.run_called_with, MagicMock))
                self.assertEqual(mock.run_call_count, call_count)

            assert_mock_called_correctly(self.before_all_mock, 1)
            assert_mock_called_correctly(self.before_each_mock, 2)
            assert_mock_called_correctly(self.after_each_mock, 2)
            assert_mock_called_correctly(self.after_all_mock, 1)

            assert_mock_called_correctly(self.scenario_mock_one, 1)
            assert_mock_called_correctly(failure_scenario, 1)

            self.assertEqual(self.call_order, [
                self.before_all_mock,
                self.before_each_mock, self.after_each_mock,
                self.before_each_mock, self.after_each_mock,
                self.after_all_mock
            ])

            self.assertEqual(feature.successes, [self.scenario_mock_one])
            self.assertEqual(feature.failures, [failure_scenario])
            self.assertFalse(feature.passed)

    @patch('jasper.feature.Context')
    def test_exception_run(self, mock_context):
        class FooBarException(Exception):
            pass

        async def failing_function(context):
            self.call_order.append(failing_function)
            raise FooBarException

        self.before_each_mock.run = failing_function

        feature = Feature('foobar',
                          scenarios=[self.scenario_mock_one, self.scenario_mock_two],
                          before_all=self.before_all_mock, after_all=self.after_all_mock,
                          before_each=self.before_each_mock, after_each=self.after_each_mock)

        self.loop.run_until_complete(feature.run())

        self.assertEqual(type(feature.exception), FooBarException)

        def assert_mock_called_correctly(mock, call_count):
            self.assertTrue(mock.run_called)
            self.assertTrue(isinstance(mock.run_called_with, MagicMock))
            self.assertEqual(mock.run_call_count, call_count)

        assert_mock_called_correctly(self.before_all_mock, 1)
        self.assertFalse(self.after_each_mock.run_called)
        assert_mock_called_correctly(self.after_all_mock, 1)

        self.assertFalse(self.scenario_mock_one.run_called)
        self.assertFalse(self.scenario_mock_two.run_called)

        self.assertEqual(self.call_order, [
            self.before_all_mock,
            failing_function,
            failing_function,
            self.after_all_mock
        ])

        self.assertFalse(feature.passed)
