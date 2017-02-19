from jasper import step, Step
import asyncio


@step
def nothing(context):
    pass


@step
def some_function(context):
    def some_function(**some_function_kwargs):
        pass

    context.function = some_function


@step
def some_kwargs(context, **kwargs):
    context.kwargs = kwargs


@step
def an_initialized_given_object(context, ran=False, passed=False, **given_function_kwargs):

    def some_function(given_function_context, **kwargs):
        context.given_function_called = True
        context.given_function_called_with = kwargs

    context.given_object = Step(some_function, **given_function_kwargs)
    context.given_object.passed = passed
    context.given_object.ran = ran


@step
def an_initialized_given_object_with_an_async_function(context, ran=False, passed=False, **given_function_kwargs):

    async def some_function(given_function_context, **kwargs):
        await asyncio.sleep(1)
        context.given_function_called = True
        context.given_function_called_with = kwargs

    context.given_object = Step(some_function, **given_function_kwargs)
    context.given_object.passed = passed
    context.given_object.ran = ran


@step
def an_initialized_given_object_with_a_function_that_will_fail(context):

    def some_function(given_function_context, **kwargs):
        raise Exception

    context.given_object = Step(some_function)


@step
def an_exception(context):
    raise Exception
