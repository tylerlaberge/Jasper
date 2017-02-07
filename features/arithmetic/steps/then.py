from jasper import Expect, then


@then
def we_will_get_a_negative_number(context):
    Expect(context.result).to_be.less_than(0)


@then
def we_will_get_a_positive_number(context):
    Expect(context.result).to_be.greater_than(0)


@then
def a_typeerror_will_occur(context):
    Expect(context.result.__class__).to_be(TypeError)


@then
def we_will_have_slept(context):
    Expect(context.result['slept']).to_be(True)
