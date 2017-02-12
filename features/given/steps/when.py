from jasper import Given, given, when, Context
from unittest import mock


@when
def we_do_nothing(context):
    pass


@when
def we_initialize_a_given_object_with_it(context):
    context.given_object = Given(context.function, **context.kwargs)


@when
async def we_run_it_with_some_context(context):
    mocked_context = mock.MagicMock(Context)()
    await context.given_object.run(mocked_context)


@when
async def we_run_it_and_are_prepared_for_an_exception(context):
    mocked_context = mock.MagicMock(Context)()
    try:
        await context.given_object.run(mocked_context)
        context.exception = None
    except Exception as e:
        context.exception = e


@when
def we_wrap_the_function_with_the_given_decorator(context):
    context.function = given(context.function)


@when
def we_call_the_given_function_with_the_given_kwargs(context):
    context.function_call_result = context.function(**context.kwargs)


@when
def we_raise_an_exception(context):
    raise Exception

