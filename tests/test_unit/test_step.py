from unittest import TestCase, mock
from jasper.step import Step, step
import time
import asyncio


class StepTestCase(TestCase):

    def setUp(self):
        self.slow_function_called = False
        self.slow_function_called_with = None

        def slow_function(context, sleep_time=0.5, fail=False):
            time.sleep(sleep_time)
            self.slow_function_called = True
            self.slow_function_called_with = {'context': context, 'sleep_time': sleep_time, 'fail': fail}

            if fail:
                raise Exception

        self.async_slow_function_called = False
        self.async_slow_function_called_with = None

        async def async_slow_function(context, sleep_time=0.5, fail=False):
            await asyncio.sleep(sleep_time)
            self.async_slow_function_called = True
            self.async_slow_function_called_with = {'context': context, 'sleep_time': sleep_time, 'fail': fail}

            if fail:
                raise Exception

        self.slow_function = slow_function
        self.async_slow_function = async_slow_function
        self.loop = asyncio.new_event_loop()

    def tearDown(self):
        self.loop.close()

    def test_init(self):
        some_step = Step(self.slow_function, sleep_time=0.1, fail=False)

        self.assertEqual(some_step.function, self.slow_function)
        self.assertEqual(some_step.kwargs, {'sleep_time': 0.1, 'fail': False})
        self.assertFalse(some_step.ran)
        self.assertFalse(some_step.passed)

    def test_successful_run(self):
        mock_context = mock.MagicMock()
        some_step = Step(self.slow_function, sleep_time=0.1, fail=False)

        try:
            self.loop.run_until_complete(some_step.run(mock_context))
        except Exception:
            raise AssertionError
        else:
            self.assertTrue(some_step.ran)
            self.assertTrue(some_step.passed)
            self.assertTrue(self.slow_function_called)
            self.assertEqual(
                self.slow_function_called_with, {'context': mock_context, 'sleep_time': 0.1, 'fail': False}
            )

    def test_failure_run(self):
        mock_context = mock.MagicMock()
        some_step = Step(self.slow_function, sleep_time=0.1, fail=True)

        with self.assertRaises(Exception):
            self.loop.run_until_complete(some_step.run(mock_context))

            self.assertTrue(some_step.ran)
            self.assertFalse(some_step.passed)
            self.assertTrue(self.slow_function_called)
            self.assertEqual(
                self.slow_function_called_with, {'context': mock_context, 'sleep_time': 0.1, 'fail': True}
            )

    def test_successful_async_run(self):
        mock_context = mock.MagicMock()
        some_step = Step(self.async_slow_function, sleep_time=0.1, fail=False)

        try:
            self.loop.run_until_complete(some_step.run(mock_context))
        except Exception:
            raise AssertionError
        else:
            self.assertTrue(some_step.ran)
            self.assertTrue(some_step.passed)
            self.assertTrue(self.async_slow_function_called)
            self.assertEqual(
                self.async_slow_function_called_with, {'context': mock_context, 'sleep_time': 0.1, 'fail': False}
            )

    def test_failure_async_run(self):
        mock_context = mock.MagicMock()
        some_step = Step(self.async_slow_function, sleep_time=0.1, fail=True)

        with self.assertRaises(Exception):
            self.loop.run_until_complete(some_step.run(mock_context))

            self.assertTrue(some_step.ran)
            self.assertFalse(some_step.passed)
            self.assertTrue(self.async_slow_function_called)
            self.assertEqual(
                self.async_slow_function_called_with, {'context': mock_context, 'sleep_time': 0.1, 'fail': True}
            )

    def test_step_decorator(self):
        some_step = step(self.slow_function)(sleep_time=0.1, fail=False)

        self.assertTrue(isinstance(some_step, Step))
        self.assertEqual(some_step.function, self.slow_function)
        self.assertEqual(some_step.kwargs, {'sleep_time': 0.1, 'fail': False})
        self.assertFalse(some_step.ran)
        self.assertFalse(some_step.passed)
