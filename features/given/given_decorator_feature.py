from jasper import Feature, Scenario
from features.given.steps.given import *
from features.given.steps.when import *
from features.given.steps.then import *


feature = Feature(
    'Given Decorator Feature',
    Scenario(
        'Decorating a function',
        given=some_function_and_kwargs(kwargs={'foo': 'bar'}),
        when=we_wrap_the_function_with_the_given_decorator_and_call_it_with_those_kwargs(),
        then=it_should_return_a_given_object_instance_with_the_function_and_those_kwargs()
    )
)