from jasper import then, Expect, Given
from jasper.utility import cyan, red


@then
def the_given_object_should_use_the_given_function(context):
    Expect(context.given_object.given_function).to_be(context.function)


@then
def the_given_object_should_use_the_given_kwargs(context):
    Expect(context.given_object.kwargs).to_equal(context.kwargs)


@then
def the_given_function_should_have_been_called_with(context, given_function_kwargs={}):
    Expect(context.given_function_called).to_be(True)
    Expect(context.given_function_called_with).to_equal(given_function_kwargs)


@then
def an_exception_should_have_been_raised(context):
    Expect(type(context.exception)).to_be(Exception)


@then
def the_given_step_should_have_passed(context):
    Expect(context.given_object.passed).to_be(True)


@then
def the_given_step_should_have_failed(context):
    Expect(context.given_object.passed).to_be(False)


@then
def the_decorated_function_should_return_a_given_object(context):
    Expect(type(context.function_call_result)).to_be(Given)


@then
def there_should_be_foo_data(context):
    Expect(context.foo).to_be('foo')


@then
def an_exception_is_raised(context):
    raise Exception