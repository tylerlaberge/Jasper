from jasper import given, Given
import asyncio


@given
def nothing(context):
    pass


@given
def some_function(context):
    def some_function(**some_function_kwargs):
        pass

    context.function = some_function


@given
def some_kwargs(context, **kwargs):
    context.kwargs = kwargs


@given
def an_initialized_given_object(context, ran=False, passed=False, **given_function_kwargs):

    def some_function(given_function_context, **kwargs):
        context.given_function_called = True
        context.given_function_called_with = kwargs

    context.given_object = Given(some_function, **given_function_kwargs)
    context.given_object.passed = passed
    context.given_object.ran = ran


@given
def an_initialized_given_object_with_an_async_function(context, ran=False, passed=False, **given_function_kwargs):

    async def some_function(given_function_context, **kwargs):
        await asyncio.sleep(1)
        context.given_function_called = True
        context.given_function_called_with = kwargs

    context.given_object = Given(some_function, **given_function_kwargs)
    context.given_object.passed = passed
    context.given_object.ran = ran


@given
def an_initialized_given_object_with_a_function_that_will_fail(context):

    def some_function(given_function_context, **kwargs):
        raise Exception

    context.given_object = Given(some_function)


@given
def an_exception(context):
    raise Exception
