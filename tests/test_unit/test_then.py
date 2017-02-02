import jasper
from unittest import TestCase


class ThenTestCase(TestCase):

    def setUp(self):
        class Then(jasper.JasperThen):
            def we_will_get_a_negative_number(self):
                assert self.context.result < 0

            def we_will_get_a_positive_number(self):
                assert self.context.result > 0

        self.then = Then

    def test_initialize(self):
        then_we_will_get_a_negative_number = self.then('we_will_get_a_negative_number')

        self.assertTrue(hasattr(then_we_will_get_a_negative_number, 'then_function'))
        self.assertEqual(
            then_we_will_get_a_negative_number.then_function,
            then_we_will_get_a_negative_number.we_will_get_a_negative_number
        )

    def test_call_success(self):
        context = jasper.Context(result=-5)
        then_we_will_get_a_negative_number = self.then('we_will_get_a_negative_number')
        then_we_will_get_a_negative_number(context)

        self.assertTrue(hasattr(then_we_will_get_a_negative_number, 'context'))
        self.assertTrue(hasattr(then_we_will_get_a_negative_number.context, 'success'))
        self.assertDictEqual(then_we_will_get_a_negative_number.context, context)

        self.assertTrue(then_we_will_get_a_negative_number.context.success)

    def test_call_failure(self):
        context = jasper.Context(result=-5)
        then_we_will_get_a_positive_number = self.then('we_will_get_a_positive_number')

        then_we_will_get_a_positive_number(context)

        self.assertTrue(hasattr(then_we_will_get_a_positive_number, 'context'))
        self.assertTrue(hasattr(then_we_will_get_a_positive_number.context, 'success'))
        self.assertDictEqual(then_we_will_get_a_positive_number.context, context)

        self.assertFalse(then_we_will_get_a_positive_number.context.success)