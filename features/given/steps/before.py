from jasper import before_each, before_all


@before_each
def setup_some_foo_data(context):
    context.foo = 'foo'


@before_each
def print_before_each(context):
    print('before_each')


@before_each
def print_context_before_each(context):
    context.before_each = 'BEFORE_EACH'
    print(f'BeforeEach: {context}')


@before_all
def print_before_all(context):
    print("before_all")


@before_all
def print_context_before_all(context):
    context.before_all = 'BEFORE_ALL'
    print(f'BeforeAll: {context}')
