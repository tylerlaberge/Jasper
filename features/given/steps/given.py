from jasper import given, Given
import asyncio


@given
def some_function_and_kwargs(context, kwargs={}):
    def some_function(**some_function_kwargs):
        pass

    context.function = some_function
    context.kwargs = kwargs


@given
def an_initialized_given_object(context, passed=False, given_function_kwargs={}):

    def some_function(given_function_context, **kwargs):
        given_function_context.given_function_called = True
        given_function_context.given_function_called_with = kwargs

    context.given_object = Given(some_function, **given_function_kwargs)
    context.given_object.passed = passed


@given
def an_initialized_given_object_with_an_async_function(context, passed=False, given_function_kwargs={}):

    async def some_function(given_function_context, **kwargs):
        await asyncio.sleep(1)
        given_function_context.given_function_called = True
        given_function_context.given_function_called_with = kwargs

    context.given_object = Given(some_function, **given_function_kwargs)
    context.given_object.passed = passed

@given
def an_initialized_given_object_with_a_function_that_will_fail(context):

    def some_function(given_function_context, **kwargs):
        raise Exception

    context.given_object = Given(some_function)

