from jasper import step


@step
def setup_some_foo_data(context):
    context.foo = 'foo'


@step
def print_before_each(context):
    print('before_each')


@step
def print_context_before_each(context):
    context.before_each = 'BEFORE_EACH'
    print(f'BeforeEach: {context}')


@step
def print_before_all(context):
    print("before_all")


@step
def print_context_before_all(context):
    context.before_all = 'BEFORE_ALL'
    print(f'BeforeAll: {context}')
