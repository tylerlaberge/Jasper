from jasper import when


@when
def we_call_it_with_two_negative_numbers(context):
    context['result'] = context['function'](-5, -5)


@when
def we_call_it_with_two_positive_numbers(context):
    context['result'] = context['function'](5, 5)


@when
def we_call_it_with_two_strings(context):
    try:
        context['function']('foo', 'bar')
    except Exception as e:
        context['result'] = e
    else:
        context['result'] = None


@when
def we_raise_an_exception(context):
    raise Exception


@when
def we_call_it_with_some_number(context):
    context['sleep'](3)
    context['slept'] = True
