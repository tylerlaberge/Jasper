import jasper
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

        self.passing_dummy_step = jasper.Step(self.passing_dummy_function, foo='bar')
        self.failing_dummy_step = jasper.Step(self.failing_dummy_function, foo='bar')

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


class GivenTestCase(TestCase):

    def setUp(self):

        @jasper.given
        def dummy_function(context):
            pass

        self.dummy_function = dummy_function

    def test_decorate(self):
        given_one = self.dummy_function()
        given_two = self.dummy_function()

        self.assertEqual(type(given_one), jasper.Given)
        self.assertEqual(type(given_two), jasper.Given)
        self.assertNotEqual(id(given_one), id(given_two))


class WhenTestCase(TestCase):

    def setUp(self):

        @jasper.when
        def dummy_function(context):
            pass

        self.dummy_function = dummy_function

    def test_decorate(self):
        when_one = self.dummy_function()
        when_two = self.dummy_function()

        self.assertEqual(type(when_one), jasper.When)
        self.assertEqual(type(when_two), jasper.When)
        self.assertNotEqual(id(when_one), id(when_two))


class ThenTestCase(TestCase):

    def setUp(self):

        @jasper.then
        def dummy_function(context):
            pass

        self.dummy_function = dummy_function

    def test_decorate(self):
        then_one = self.dummy_function()
        then_two = self.dummy_function()

        self.assertEqual(type(then_one), jasper.Then)
        self.assertEqual(type(then_two), jasper.Then)
        self.assertNotEqual(id(then_one), id(then_two))


class BeforeEachTestCase(TestCase):

    def setUp(self):

        @jasper.before_each
        def dummy_function(context):
            pass

        self.dummy_function = dummy_function

    def test_decorate(self):
        before_each_one = self.dummy_function()
        before_each_two = self.dummy_function()

        self.assertEqual(type(before_each_one), jasper.BeforeEach)
        self.assertEqual(type(before_each_two), jasper.BeforeEach)
        self.assertNotEqual(id(before_each_one), id(before_each_two))


class AfterEachTestCase(TestCase):

    def setUp(self):

        @jasper.after_each
        def dummy_function(context):
            pass

        self.dummy_function = dummy_function

    def test_decorate(self):
        after_each_one = self.dummy_function()
        after_each_two = self.dummy_function()

        self.assertEqual(type(after_each_one), jasper.AfterEach)
        self.assertEqual(type(after_each_two), jasper.AfterEach)
        self.assertNotEqual(id(after_each_one), id(after_each_two))
