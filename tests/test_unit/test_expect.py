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
        self.assertIsNone(expect_object.operator)

    def test_to_be(self):
        expect_object = Expect(self.data).to_be

        self.assertTrue(expect_object.operator, 'to_be')
        self.assertFalse(expect_object.negate)

    def test_to_equal(self):
        expect_object = Expect(self.data).to_equal

        self.assertEqual(expect_object.operator, 'to_equal')
        self.assertFalse(expect_object.negate)

    def test_not(self):
        expect_object = Expect(self.data).not_

        self.assertTrue(expect_object.negate)

    def test_not_to_be(self):
        expect_object = Expect(self.data).not_.to_be

        self.assertTrue(expect_object.negate)
        self.assertEqual(expect_object.operator, 'to_be')

    def test_successful_to_be_call(self):
        expect_object = Expect(self.data)
        expect_object.operator = 'to_be'
        expect_object.negate = False

        try:
            expect_object(self.data)
        except ExpectationException:
            raise AssertionError

    def test_failure_to_be_call(self):
        expect_object = Expect(self.data)
        expect_object.operator = 'to_be'
        expect_object.negate = False

        with self.assertRaises(ExpectationException):
            expect_object({'foo': 'bar'})

    def test_successful_not_to_be_call(self):
        expect_object = Expect(self.data)
        expect_object.operator = 'to_be'
        expect_object.negate = True

        try:
            expect_object({'foo': 'bar'})
        except ExpectationException:
            raise AssertionError

    def test_failure_not_to_be_call(self):
        expect_object = Expect(self.data)
        expect_object.operator = 'to_be'
        expect_object.negate = True

        with self.assertRaises(ExpectationException):
            expect_object(self.data)

    def test_successful_to_equal_call(self):
        expect_object = Expect(self.data)
        expect_object.operator = 'to_equal'
        expect_object.negate = False

        try:
            expect_object({'foo': 'bar'})
        except ExpectationException:
            raise AssertionError

    def test_failure_to_equal_call(self):
        expect_object = Expect(self.data)
        expect_object.operator = 'to_equal'
        expect_object.negate = False

        with self.assertRaises(ExpectationException):
            expect_object('foo')

    def test_successful_not_to_equal(self):
        expect_object = Expect(self.data)
        expect_object.operator = 'to_equal'
        expect_object.negate = True

        try:
            expect_object('foo')
        except ExpectationException:
            raise AssertionError

    def test_failure_not_to_equal(self):
        expect_object = Expect(self.data)
        expect_object.operator = 'to_equal'
        expect_object.negate = True

        with self.assertRaises(ExpectationException):
            expect_object({'foo': 'bar'})

    def test_successful_to_be_less_than(self):
        expect_object = Expect(10)
        expect_object.operator = 'to_be'
        expect_object.negate = False

        try:
            expect_object.less_than(15)
        except ExpectationException:
            raise AssertionError

    def test_failure_to_be_less_than(self):
        expect_object = Expect(10)
        expect_object.operator = 'to_be'
        expect_object.negate = False

        with self.assertRaises(ExpectationException):
            expect_object(5)

    def test_successful_not_to_be_less_than(self):
        expect_object = Expect(10)
        expect_object.operator = 'to_be'
        expect_object.negate = True

        try:
            expect_object(5)
        except ExpectationException:
            raise AssertionError

    def test_failure_not_to_be_less_than(self):
        expect_object = Expect(10)
        expect_object.operator = 'to_be'
        expect_object.negate = True

        with self.assertRaises(ExpectationException):
            expect_object.less_than(15)

    def test_successful_to_be_greater_than(self):
        expect_object = Expect(10)
        expect_object.operator = 'to_be'
        expect_object.negate = False

        try:
            expect_object.greater_than(5)
        except ExpectationException:
            raise AssertionError

    def test_failure_to_be_greater_than(self):
        expect_object = Expect(10)
        expect_object.operator = 'to_be'
        expect_object.negate = False

        with self.assertRaises(ExpectationException):
            expect_object.greater_than(15)

    def test_successful_not_to_be_greater_than(self):
        expect_object = Expect(10)
        expect_object.operator = 'to_be'
        expect_object.negate = True

        try:
            expect_object.greater_than(15)
        except ExpectationException:
            raise AssertionError

    def test_failure_not_to_be_greater_than(self):
        expect_object = Expect(10)
        expect_object.operator = 'to_be'
        expect_object.negate = True

        with self.assertRaises(ExpectationException):
            expect_object.greater_than(5)
