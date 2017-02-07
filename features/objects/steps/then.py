from jasper import then, Expect


@then
def this_will_fail_and_we_should_see_the_object(context):
    Expect(context.object).to_be('foobar')
