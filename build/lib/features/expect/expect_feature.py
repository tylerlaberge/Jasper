from jasper import Feature, Scenario
from features.expect.steps.given import *
from features.expect.steps.when import *
from features.expect.steps.then import *


feature = Feature(
    'Expect',
    scenarios=[
        Scenario(
            'Initialization',
            given=a_number_as_our_actual_data(number=5),
            when=we_init_an_expect_object_with_our_actual_data(),
            then=the_expect_object_will_use_our_actual_data()
        ),
        Scenario(
            'Not modifier',
            given=an_initialized_expect_object(),
            when=we_use_the_modifier_(modifier='not_'),
            then=the_expect_objects_negate_attribute_will_be_(negate=True)
        ),
        Scenario(
            'ToBe operator',
            given=an_initialized_expect_object(),
            when=we_use_the_operator_(operator='to_be'),
            then=the_expect_objects_operator_attribute_will_be(operator='to_be')
        ),
        Scenario(
            'ToEqual operator',
            given=an_initialized_expect_object(),
            when=we_use_the_operator_(operator='to_equal'),
            then=the_expect_objects_operator_attribute_will_be(operator='to_equal')
        ),
        Scenario(
            'Passing ToBe Call',
            given=an_initialized_expect_object(actual_data='foo', operator='to_be'),
            when=we_call_the_expect_object_with_the_expected_data(expected_data='foo'),
            then=the_expectation_should_pass()
        ),
        Scenario(
            'Passing NotToBe Call',
            given=an_initialized_expect_object(actual_data='foo', operator='to_be', negate=True),
            when=we_call_the_expect_object_with_the_expected_data(expected_data='bar'),
            then=the_expectation_should_pass()
        ),
        Scenario(
            'Failing ToBe Call',
            given=an_initialized_expect_object(actual_data='foo', operator='to_be'),
            when=we_call_the_expect_object_with_the_expected_data(expected_data='bar'),
            then=the_expectation_should_fail()
        ),
        Scenario(
            'Failing NotToBe Call',
            given=an_initialized_expect_object(actual_data='foo', operator='to_be', negate=True),
            when=we_call_the_expect_object_with_the_expected_data(expected_data='foo'),
            then=the_expectation_should_fail()
        ),
        Scenario(
            'Passing ToEqual Call',
            given=an_initialized_expect_object(actual_data={'foo': 'bar'}, operator='to_equal'),
            when=we_call_the_expect_object_with_the_expected_data(expected_data={'foo': 'bar'}),
            then=the_expectation_should_pass()
        ),
        Scenario(
            'Passing NotToEqual Call',
            given=an_initialized_expect_object(actual_data={'foo': 'bar'}, operator='to_equal', negate=True),
            when=we_call_the_expect_object_with_the_expected_data(expected_data={'bar': 'foo'}),
            then=the_expectation_should_pass()
        ),
        Scenario(
            'Failing ToEqual Call',
            given=an_initialized_expect_object(actual_data={'foo': 'bar'}, operator='to_equal'),
            when=we_call_the_expect_object_with_the_expected_data(expected_data={'bar': 'foo'}),
            then=the_expectation_should_fail()
        ),
        Scenario(
            'Failing NotToEqual Call',
            given=an_initialized_expect_object(actual_data={'foo': 'bar'}, operator='to_equal', negate=True),
            when=we_call_the_expect_object_with_the_expected_data(expected_data={'foo': 'bar'}),
            then=the_expectation_should_fail()
        ),
        Scenario(
            'Passing ToBeLessThan',
            given=an_initialized_expect_object(actual_data=5, operator='to_be'),
            when=we_expect_the_expected_data_to_be_less_than(expected_data=10),
            then=the_expectation_should_pass()
        ),
        Scenario(
            'Passing NotToBeLessThan',
            given=an_initialized_expect_object(actual_data=5, operator='to_be', negate=True),
            when=we_expect_the_expected_data_to_be_less_than(expected_data=3),
            then=the_expectation_should_pass()
        ),
        Scenario(
            'Failing ToBeLessThan',
            given=an_initialized_expect_object(actual_data=5, operator='to_be'),
            when=we_expect_the_expected_data_to_be_less_than(expected_data=3),
            then=the_expectation_should_fail()
        ),
        Scenario(
            'Failing NotToBeLessThan',
            given=an_initialized_expect_object(actual_data=5, operator='to_be', negate=True),
            when=we_expect_the_expected_data_to_be_less_than(expected_data=10),
            then=the_expectation_should_fail()
        ),
        Scenario(
            'Passing ToBeGreaterThan',
            given=an_initialized_expect_object(actual_data=5, operator='to_be'),
            when=we_expect_the_expected_data_to_be_greater_than(expected_data=3),
            then=the_expectation_should_pass()
        ),
        Scenario(
            'Passing NotToBeGreaterThan',
            given=an_initialized_expect_object(actual_data=5, operator='to_be', negate=True),
            when=we_expect_the_expected_data_to_be_greater_than(expected_data=10),
            then=the_expectation_should_pass()
        ),
        Scenario(
            'Failing ToBeGreaterThan',
            given=an_initialized_expect_object(actual_data=5, operator='to_be'),
            when=we_expect_the_expected_data_to_be_greater_than(expected_data=10),
            then=the_expectation_should_fail()
        ),
        Scenario(
            'Failing NotToBeGreaterThan',
            given=an_initialized_expect_object(actual_data=5, operator='to_be', negate=True),
            when=we_expect_the_expected_data_to_be_greater_than(expected_data=3),
            then=the_expectation_should_fail()
        )
    ]
)
