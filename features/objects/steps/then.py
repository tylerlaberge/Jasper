from jasper import then, Expect


@then
def this_will_fail_and_we_should_see_the_object(context):
    Expect(context.object).to_be('foobar')


@then
def the_two_unique_objects_will_have_identical_contents(context):
    Expect(context.object).not_.to_be(context.result)
    Expect(context.object).to_equal(context.result)
