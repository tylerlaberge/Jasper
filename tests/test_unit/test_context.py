from unittest import TestCase
from jasper.context import Context


class ContextTestCase(TestCase):

    def test_empty_init(self):
        context = Context()

        self.assertEqual(context.__dict__, {'_items': {}})

    def test_init_with_kwargs(self):
        context = Context(foo='bar', foobar='barfoo')

        self.assertEqual(context.__dict__, {'_items': {'foo': 'bar', 'foobar': 'barfoo'}})

    def test_get_attr(self):
        context = Context()
        context.__dict__['_items'] = {'foobar': 'barfoo'}

        try:
            foobar = context.foobar
        except AttributeError:
            raise AssertionError
        else:
            self.assertEqual(foobar, 'barfoo')

    def test_get_missing_attr(self):
        context = Context()

        with self.assertRaises(AttributeError):
            foobar = context.foobar

    def test_set_attr(self):
        context = Context()
        context.foobar = 'barfoo'

        self.assertEqual(context.__dict__['_items'], {'foobar': 'barfoo'})

    def test_str(self):
        context = Context()
        context.__dict__['_items'] = {'foo': 'bar', 'foobar': 'barfoo'}

        self.assertEqual(str({'foo': 'bar', 'foobar': 'barfoo'}), str(context))

    def test_copy(self):
        context = Context()
        context.__dict__['_items'] = {'foo': 'bar', 'foobar': 'barfoo', 'some_dict': {'some_foo': 'some_bar'}}

        context_copy = context.copy()

        self.assertIsNot(context, context_copy)
        self.assertEqual(context.__dict__, context_copy.__dict__)
        self.assertIsNot(context.__dict__['_items']['some_dict'], context_copy.__dict__['_items']['some_dict'])
