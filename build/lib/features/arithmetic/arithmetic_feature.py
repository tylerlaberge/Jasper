from jasper import Feature, Scenario
from features.arithmetic.steps.given import *
from features.arithmetic.steps.when import *
from features.arithmetic.steps.then import *


feature = Feature(
    'Arithmetic',
    scenarios=[
        Scenario(
            'Adding two numbers',
            given=an_adding_function(),
            when=we_call_it_with_two_numbers(a=5, b=10),
            then=the_two_numbers_numbers_should_have_been_added_together(a=5, b=10)
        )
    ]
)
