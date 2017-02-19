from jasper import Step
from unittest import TestCase, mock
import asyncio


class StepTestCase(TestCase):

    def setUp(self):

        self.called = False
        self.called_with_args = None
        self.called_with_kwargs = None

        def passing_dummy_function(context, **kwargs):
            self.called = True
            self.called_with_args = context
            self.called_with_kwargs = kwargs

        def failing_dummy_function(context, **kwargs):
            raise Exception

        self.passing_dummy_function = passing_dummy_function
        self.failing_dummy_function = failing_dummy_function

        self.passing_dummy_step = Step(self.passing_dummy_function, foo='bar')
        self.failing_dummy_step = Step(self.failing_dummy_function, foo='bar')

    def test_initialize(self):
        self.assertEqual(self.passing_dummy_step.function, self.passing_dummy_function)
        self.assertEqual(self.passing_dummy_step.kwargs, {'foo': 'bar'})
        self.assertFalse(self.passing_dummy_step.ran)
        self.assertFalse(self.passing_dummy_step.passed)

    @mock.patch('jasper.Context')
    def test_call_success(self, mock_context):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.passing_dummy_step.run(mock_context))

        self.assertTrue(self.called)
        self.assertEqual(self.called_with_args, mock_context)
        self.assertEqual(self.called_with_kwargs, {'foo': 'bar'})
        self.assertTrue(self.passing_dummy_step.ran)
        self.assertTrue(self.passing_dummy_step.passed)

    @mock.patch('jasper.Context')
    def test_call_fail(self, mock_context):
        loop = asyncio.get_event_loop()

        with self.assertRaises(Exception):
            loop.run_until_complete(self.failing_dummy_step.run(mock_context))
            self.assertTrue(self.failing_dummy_step.ran)
            self.assertFalse(self.failing_dummy_step.passed)
