from unittest import TestCase
from jasper.expect import Expect
from jasper.exceptions import ExpectationException


class ExpectTestCase(TestCase):

    def setUp(self):
        self.data = {'foo': 'bar'}

    def test_initialize(self):
        expect_object = Expect(self.data)

        self.assertEqual(expect_object.actual_data, self.data)
        self.assertFalse(expect_object.negate)

    def test_not(self):
        expect_object = Expect(self.data).not_()

        self.assertTrue(expect_object.negate)

    def test_successful_to_be(self):
        expect_object = Expect(self.data)
        expect_object.negate = False

        try:
            expect_object.to_be(self.data)
        except ExpectationException:
            raise AssertionError

    def test_failure_to_be_call(self):
        expect_object = Expect(self.data)
        expect_object.negate = False

        with self.assertRaises(ExpectationException):
            expect_object.to_be({'foo': 'bar'})

    def test_successful_not_to_be_call(self):
        expect_object = Expect(self.data)
        expect_object.negate = True

        try:
            expect_object.to_be({'foo': 'bar'})
        except ExpectationException:
            raise AssertionError

    def test_failure_not_to_be_call(self):
        expect_object = Expect(self.data)
        expect_object.negate = True

        with self.assertRaises(ExpectationException):
            expect_object.to_be(self.data)

    def test_successful_to_equal_call(self):
        expect_object = Expect(self.data)
        expect_object.negate = False

        try:
            expect_object.to_equal({'foo': 'bar'})
        except ExpectationException:
            raise AssertionError

    def test_failure_to_equal_call(self):
        expect_object = Expect(self.data)
        expect_object.negate = False

        with self.assertRaises(ExpectationException):
            expect_object.to_equal('foo')

    def test_successful_not_to_equal(self):
        expect_object = Expect(self.data)
        expect_object.negate = True

        try:
            expect_object.to_equal('foo')
        except ExpectationException:
            raise AssertionError

    def test_failure_not_to_equal(self):
        expect_object = Expect(self.data)
        expect_object.negate = True

        with self.assertRaises(ExpectationException):
            expect_object.to_equal({'foo': 'bar'})

    def test_successful_to_be_less_than(self):
        expect_object = Expect(10)
        expect_object.negate = False

        try:
            expect_object.to_be_less_than(15)
        except ExpectationException:
            raise AssertionError

    def test_failure_to_be_less_than(self):
        expect_object = Expect(10)
        expect_object.negate = False

        with self.assertRaises(ExpectationException):
            expect_object.to_be_less_than(5)

    def test_successful_not_to_be_less_than(self):
        expect_object = Expect(10)
        expect_object.negate = True

        try:
            expect_object.to_be_less_than(5)
        except ExpectationException:
            raise AssertionError

    def test_failure_not_to_be_less_than(self):
        expect_object = Expect(10)
        expect_object.negate = True

        with self.assertRaises(ExpectationException):
            expect_object.to_be_less_than(15)

    def test_successful_to_be_greater_than(self):
        expect_object = Expect(10)
        expect_object.negate = False

        try:
            expect_object.to_be_greater_than(5)
        except ExpectationException:
            raise AssertionError

    def test_failure_to_be_greater_than(self):
        expect_object = Expect(10)
        expect_object.negate = False

        with self.assertRaises(ExpectationException):
            expect_object.to_be_greater_than(15)

    def test_successful_not_to_be_greater_than(self):
        expect_object = Expect(10)
        expect_object.negate = True

        try:
            expect_object.to_be_greater_than(15)
        except ExpectationException:
            raise AssertionError

    def test_failure_not_to_be_greater_than(self):
        expect_object = Expect(10)
        expect_object.negate = True

        with self.assertRaises(ExpectationException):
            expect_object.to_be_greater_than(5)

    def test_successful_to_be_less_than_or_equal_to(self):
        expect_object = Expect(10)
        expect_object.negate = False

        try:
            expect_object.to_be_less_than_or_equal_to(15)
            expect_object.to_be_less_than_or_equal_to(10)
        except ExpectationException:
            raise AssertionError

    def test_failure_to_be_less_than_or_equal_to(self):
        expect_object = Expect(10)
        expect_object.negate = False

        with self.assertRaises(ExpectationException):
            expect_object.to_be_less_than_or_equal_to(9)

    def test_successful_not_to_be_less_than_or_equal_to(self):
        expect_object = Expect(10)
        expect_object.negate = True

        try:
            expect_object.to_be_less_than_or_equal_to(9)
        except ExpectationException:
            raise AssertionError

    def test_failure_not_to_be_less_than_or_equal_to(self):
        expect_object = Expect(10)
        expect_object.negate = True

        with self.assertRaises(ExpectationException):
            expect_object.to_be_less_than_or_equal_to(10)

        with self.assertRaises(ExpectationException):
            expect_object.to_be_less_than_or_equal_to(15)

    def test_successful_to_be_greater_than_or_equal_to(self):
        expect_object = Expect(10)
        expect_object.negate = False

        try:
            expect_object.to_be_greater_than_or_equal_to(5)
            expect_object.to_be_greater_than_or_equal_to(10)
        except ExpectationException:
            raise AssertionError

    def test_failure_to_be_greater_than_or_equal_to(self):
        expect_object = Expect(10)
        expect_object.negate = False

        with self.assertRaises(ExpectationException):
            expect_object.to_be_greater_than_or_equal_to(11)

    def test_successful_not_to_be_greater_than_or_equal_to(self):
        expect_object = Expect(10)
        expect_object.negate = True

        try:
            expect_object.to_be_greater_than_or_equal_to(11)
        except ExpectationException:
            raise AssertionError

    def test_failure_not_to_be_greater_than_or_equal_to(self):
        expect_object = Expect(10)
        expect_object.negate = True

        with self.assertRaises(ExpectationException):
            expect_object.to_be_greater_than_or_equal_to(5)

        with self.assertRaises(ExpectationException):
            expect_object.to_be_greater_than_or_equal_to(10)
