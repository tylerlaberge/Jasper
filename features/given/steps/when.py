from jasper import Given, given, when, Context, GivenException
from unittest import mock


@when
def we_initialize_a_given_object_with_it(context):
    return Given(context.function, **context.kwargs)


@when
async def we_run_it_with_some_context(context):
    mocked_context = mock.MagicMock(Context)()
    await context.given_object.run(mocked_context)
    return mocked_context


@when
async def we_run_it_and_are_prepared_for_an_exception(context):
    mocked_context = mock.MagicMock(Context)()
    try:
        await context.given_object.run(mocked_context)
        return None
    except GivenException as e:
        return e


@when
def we_get_a_string_representation_of_the_given_object(context):
    return str(context.given_object)


@when
def we_wrap_the_function_with_the_given_decorator_and_call_it_with_those_kwargs(context):
    return given(context.function)(**context.kwargs)
