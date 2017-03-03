from jasper import step


@step
def teardown_some_foo_data(context):
    context.foo = None


@step
def print_after_each(context):
    print('after_each')


@step
def print_context_after_each(context):
    context.after_each = 'AFTER_EACH'
    print(f'AfterEach: {context}')


@step
def print_after_all(context):
    print('after_all')


@step
def print_context_after_all(context):
    context.after_all = 'AFTER_ALL'
    print(f'AfterAll: {context}')

