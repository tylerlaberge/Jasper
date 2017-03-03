from unittest import TestCase
from unittest.mock import MagicMock
from jasper.scenario import Scenario
from jasper.steps import Step
from jasper.exceptions import ValidationException
import asyncio


class ScenarioTestCase(TestCase):

    def setUp(self):
        mock_step = MagicMock(spec=Step)

        call_order = []

        class StepMock(mock_step.__class__):

            def __init__(self):
                self.run_called = False
                self.run_called_with = None
                self.run_call_count = 0

            async def run(self, context):
                self.run_called = True
                self.run_called_with = context
                self.run_call_count += 1
                call_order.append(self)

        self.call_order = call_order

        self.given_mock_one = StepMock()
        self.given_mock_two = StepMock()
        self.when_mock = StepMock()
        self.then_mock = StepMock()
        self.before_all_mock = StepMock()
        self.after_all_mock = StepMock()
        self.before_each_mock = StepMock()
        self.after_each_mock = StepMock()
        self.loop = asyncio.new_event_loop()

    def tearDown(self):
        self.loop.close()

    def test_init(self):
        scenario = Scenario('foobar',
                            given=[self.given_mock_one, self.given_mock_two], when=self.when_mock, then=self.then_mock,
                            before_all=self.before_all_mock, after_all=self.after_all_mock,
                            before_each=self.before_each_mock, after_each=self.after_each_mock)

        self.assertEqual(scenario.description, 'foobar')
        self.assertEqual(scenario.given, [self.given_mock_one, self.given_mock_two])
        self.assertEqual(scenario.when, [self.when_mock])
        self.assertEqual(scenario.then, [self.then_mock])
        self.assertEqual(scenario.before_each, [self.before_each_mock])
        self.assertEqual(scenario.before_all, [self.before_all_mock])
        self.assertEqual(scenario.after_each, [self.after_each_mock])
        self.assertEqual(scenario.after_all, [self.after_all_mock])
        self.assertIsNone(scenario.exception)
        self.assertFalse(scenario.ran)
        self.assertFalse(scenario.passed)

    def test_init_validation_error(self):
        try:
            scenario = Scenario('foobar', given='some_given', when='some_when', then=lambda: 'some_then')
        except ValidationException as e:
            self.assertEqual(str(e), "\n\nScenario 'foobar'. Given: 'some_given' must be an initialized Step object. "
                                     "Instead got '<class 'str'>'. Did you call the decorated step function?")
        else:
            raise AssertionError()

    def test_successful_run(self):
        mock_context = MagicMock()
        scenario = Scenario('foobar',
                            given=[self.given_mock_one, self.given_mock_two], when=self.when_mock, then=self.then_mock,
                            before_all=self.before_all_mock, after_all=self.after_all_mock,
                            before_each=self.before_each_mock, after_each=self.after_each_mock)

        try:
            self.loop.run_until_complete(scenario.run(mock_context))
        except Exception:
            raise AssertionError
        else:
            self.assertTrue(scenario.ran)
            self.assertTrue(scenario.passed)

            def assert_step_mock_called_correctly(step_mock, call_count):
                self.assertTrue(step_mock.run_called)
                self.assertEqual(step_mock.run_called_with, mock_context)
                self.assertEqual(step_mock.run_call_count, call_count)

            assert_step_mock_called_correctly(self.before_all_mock, 1)
            assert_step_mock_called_correctly(self.before_each_mock, 4)
            assert_step_mock_called_correctly(self.after_each_mock, 4)
            assert_step_mock_called_correctly(self.after_all_mock, 1)

            assert_step_mock_called_correctly(self.given_mock_one, 1)
            assert_step_mock_called_correctly(self.given_mock_two, 1)
            assert_step_mock_called_correctly(self.when_mock, 1)
            assert_step_mock_called_correctly(self.then_mock, 1)

            self.assertEqual(self.call_order, [
                self.before_all_mock,
                self.before_each_mock, self.given_mock_one, self.after_each_mock,
                self.before_each_mock, self.given_mock_two, self.after_each_mock,
                self.before_each_mock, self.when_mock, self.after_each_mock,
                self.before_each_mock, self.then_mock, self.after_each_mock,
                self.after_all_mock
            ])

    def test_failure_run(self):
        mock_context = MagicMock()

        class FooBarException(Exception):
            pass

        async def failing_function(context):
            self.call_order.append(failing_function)
            raise FooBarException

        self.when_mock.run = failing_function

        scenario = Scenario('foobar',
                            given=[self.given_mock_one, self.given_mock_two], when=self.when_mock, then=self.then_mock,
                            before_all=self.before_all_mock, after_all=self.after_all_mock,
                            before_each=self.before_each_mock, after_each=self.after_each_mock)

        self.loop.run_until_complete(scenario.run(mock_context))
        self.assertTrue(scenario.ran)
        self.assertFalse(scenario.passed)
        self.assertEqual(type(scenario.exception), FooBarException)

        def assert_step_mock_called_correctly(step_mock, call_count):
            self.assertTrue(step_mock.run_called)
            self.assertEqual(step_mock.run_called_with, mock_context)
            self.assertEqual(step_mock.run_call_count, call_count)

        assert_step_mock_called_correctly(self.before_all_mock, 1)
        assert_step_mock_called_correctly(self.before_each_mock, 3)
        assert_step_mock_called_correctly(self.after_each_mock, 3)
        assert_step_mock_called_correctly(self.after_all_mock, 1)

        assert_step_mock_called_correctly(self.given_mock_one, 1)
        assert_step_mock_called_correctly(self.given_mock_two, 1)

        self.assertFalse(self.then_mock.run_called)
        self.assertEqual(self.call_order, [
            self.before_all_mock,
            self.before_each_mock, self.given_mock_one, self.after_each_mock,
            self.before_each_mock, self.given_mock_two, self.after_each_mock,
            self.before_each_mock, failing_function, self.after_each_mock,
            self.after_all_mock
        ])
