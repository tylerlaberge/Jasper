from unittest import TestCase
from jasper import Expect
from jasper.exceptions import ExpectationException


class ExpectTestCase(TestCase):

    def setUp(self):
        self.number = 5

    def test_initialize(self):
        expect_object = Expect(self.number)

        self.assertEqual(self.number, expect_object.actual_data)

    def test_successful_to_be(self):
        Expect(self.number).to_be(self.number)

    def test_failure_to_be(self):
        with self.assertRaises(ExpectationException) as e:
            Expect(self.number).to_be(self.number + 1)

            self.assertEqual(e.actual, self.number)
            self.assertEqual(e.expected, self.number + 1)

    def test_successful_to_be_less_than(self):
        Expect(self.number).to_be.less_than(self.number + 1)

    def test_failure_to_be_less_than(self):
        with self.assertRaises(ExpectationException) as e:
            Expect(self.number).to_be.less_than(self.number)

            self.assertEqual(e.actual, self.number)
            self.assertEqual(e.expected, self.number)

    def test_successful_to_be_greater_than(self):
        Expect(self.number).to_be.greater_than(self.number - 1)

    def test_failure_to_be_greater_than(self):
        with self.assertRaises(ExpectationException) as e:
            Expect(self.number).to_be.greater_than(self.number)

            self.assertEqual(e.actual, self.number)
            self.assertEqual(e.expected, self.number)