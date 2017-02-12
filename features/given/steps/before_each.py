from jasper import before_each


@before_each
def prepare_some_foo_data(context):
    context.foo = 'foo'
