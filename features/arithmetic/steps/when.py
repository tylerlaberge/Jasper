from jasper import when


@when
def we_call_it_with_two_negative_numbers(context):
    return context.function(-5, -5)


@when
def we_call_it_with_two_positive_numbers(context):
    return context.function(5, 5)


@when
def we_call_it_with_two_strings(context):
    try:
        context.function('foo', 'bar')
    except Exception as e:
        return e
    else:
        return None


@when
def we_raise_an_exception(context):
    raise Exception


@when
async def we_call_it_with_the_number_5(context):
    await context.sleep(5)
    return {'slept': True}
