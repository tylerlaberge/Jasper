from jasper import step


@step
def an_adding_function(context):
    context.function = lambda a, b: a + b