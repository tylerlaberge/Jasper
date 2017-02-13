from jasper import after_each


@after_each
def teardown_some_foo_data(context):
    context.foo = None
    print('after')
