from jasper import Feature, Scenario
from features.given.steps.given import *
from features.given.steps.when import *
from features.given.steps.then import *
from features.given.steps.before import *
from features.given.steps.after import *


feature = Feature(
    'Given Decorator Feature',
    before_all=setup_some_foo_data(),
    after_all=teardown_some_foo_data(),
    before_each=setup_some_foo_data(),
    after_each=teardown_some_foo_data(),
    scenarios=[
        Scenario(
            'Decorating a function',
            before_all=setup_some_foo_data(),
            before_each=setup_some_foo_data(),
            after_each=teardown_some_foo_data(),
            after_all=teardown_some_foo_data(),
            given=[
                some_function(),
                some_kwargs(kwargs={'foo': 'bar'})
            ],
            when=[
                we_wrap_the_function_with_the_given_decorator(),
                we_call_the_given_function_with_the_given_kwargs()
            ],
            then=the_decorated_function_should_return_a_given_object()
        )
    ]
)
