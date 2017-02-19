from jasper import step, Expect


@step
def a_number_as_our_actual_data(context, number):
    context.actual_data = number


@step
def an_initialized_expect_object(context, actual_data='foo', negate=False, operator=None):
    expect = Expect(actual_data)
    expect.negate = negate
    expect.operator = operator

    context.expect = expect
