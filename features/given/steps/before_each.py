from jasper import before_each


@before_each
def setup_some_foo_data(context):
    context.foo = 'foo'
    print('before')

