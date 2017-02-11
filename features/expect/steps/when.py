from jasper import when, Expect, ExpectationException


@when
def we_init_an_expect_object_with_our_actual_data(context):
    return Expect(context.actual_data)


@when
def we_use_the_modifier_(context, modifier):
    return getattr(context.expect, modifier)


@when
def we_use_the_operator_(context, operator):
    return getattr(context.expect, operator)


@when
def we_call_the_expect_object_with_the_expected_data(context, expected_data):
    try:
        return context.expect(expected_data)
    except ExpectationException as e:
        return e


@when
def we_expect_the_expected_data_to_be_less_than(context, expected_data):
    try:
        return context.expect.less_than(expected_data)
    except ExpectationException as e:
        return e


@when
def we_expect_the_expected_data_to_be_greater_than(context, expected_data):
    try:
        return context.expect.greater_than(expected_data)
    except ExpectationException as e:
        return e
