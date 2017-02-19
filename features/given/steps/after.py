from jasper import after_each, after_all


@after_each
def teardown_some_foo_data(context):
    context.foo = None


@after_each
def print_after_each(context):
    print('after_each')


@after_each
def print_context_after_each(context):
    context.after_each = 'AFTER_EACH'
    print(f'AfterEach: {context}')


@after_all
def print_after_all(context):
    print('after_all')


@after_all
def print_context_after_all(context):
    context.after_all = 'AFTER_ALL'
    print(f'AfterAll: {context}')

