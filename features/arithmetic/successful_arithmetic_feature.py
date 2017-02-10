from jasper import Feature, Scenario
from features.arithmetic.steps.given import *
from features.arithmetic.steps.when import *
from features.arithmetic.steps.then import *


feature = Feature(
    'Slow Feature',
    Scenario(
        'Slow Scenario',
        given=a_slow_function(),
        when=we_call_it_with(seconds=1),
        then=we_will_have_slept_for(seconds=1)
    ),
    Scenario(
        'Slow Scenario Two',
        given=a_slow_function(),
        when=we_call_it_with(seconds=3),
        then=we_will_have_slept_for(seconds=3)
    )
)
feature_two = Feature(
    'Slow Feature Two',
    Scenario(
        'Slow Scenario Three',
        given=a_slow_function(),
        when=we_call_it_with(seconds=5),
        then=we_will_have_slept_for(seconds=5)
    ),
    Scenario(
        'Slow Scenario Four',
        given=a_slow_function(),
        when=we_call_it_with(seconds=7),
        then=we_will_have_slept_for(seconds=7)
    )
)
feature_three = Feature(
    'Successful Arithmetic',
    Scenario(
        'Adding two negative numbers',
        given=an_adding_function(),
        when=we_call_it_with_two_positive_numbers(),
        then=we_will_get_a_positive_number()
    ),
    Scenario(
        'Multiplying two negative numbers',
        given=a_multiplication_function(),
        when=we_call_it_with_two_negative_numbers(),
        then=we_will_get_a_positive_number()
    )
)
