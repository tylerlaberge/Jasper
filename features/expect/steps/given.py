from jasper import given, Expect


@given
def a_number_as_our_actual_data(context, number):
    context.actual_data = number


@given
def an_initialized_expect_object(context, actual_data='foo', negate=False, operator=None):
    expect = Expect(actual_data)
    expect.negate = negate
    expect.operator = operator

    context.expect = expect
