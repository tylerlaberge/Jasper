from jasper import step


@step
def we_call_it_with_two_numbers(context, a, b):
    context.result = context.function(a, b)
