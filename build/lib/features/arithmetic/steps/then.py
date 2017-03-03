from jasper import step, Expect


@step
def the_two_numbers_numbers_should_have_been_added_together(context, a, b):
    Expect(context.result).to_be(a + b)
