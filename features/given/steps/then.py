from jasper import then, Expect, GivenException, Given
from jasper.utility import cyan, red


@then
def the_given_object_will_use_that_function_and_kwargs(context):
    Expect(context.result.given_function).to_be(context.function)
    Expect(context.result.kwargs).to_equal(context.kwargs)


@then
def the_given_function_should_have_passed_and_been_called_with(context, given_function_kwargs={}):
    Expect(context.given_object.passed).to_be(True)
    Expect(context.result.given_function_called).to_be(True)
    Expect(context.result.given_function_called_with).to_equal(given_function_kwargs)


@then
def a_given_exception_should_have_been_raised_and_the_given_object_should_have_passed(context):
    Expect(type(context.result)).to_be(GivenException)
    Expect(context.given_object.passed).to_be(False)


@then
def it_should_be_colored_cyan_and_display_its_attributes(context, given_function_kwargs={}):
    Expect(context.result).to_equal(cyan(f'Given: some_function {given_function_kwargs}'))


@then
def it_should_be_colored_red_and_display_its_attributes(context, given_function_kwargs={}):
    Expect(context.result).to_equal(red(f'Given: some_function {given_function_kwargs}'))


@then
def it_should_return_a_given_object_instance_with_the_function_and_those_kwargs(context):
    Expect(type(context.result)).to_be(Given)
    Expect(context.result.given_function).to_be(context.function)
    Expect(context.result.kwargs).to_equal(context.kwargs)

