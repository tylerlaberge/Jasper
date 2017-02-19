from jasper import Feature, Scenario
from features.given.steps.given import *
from features.given.steps.when import *
from features.given.steps.then import *


feature = Feature(
    'Given Decorator Feature',
    scenarios=[
        Scenario(
            'Decorating a function',
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
