from jasper import Feature, Scenario
from features.arithmetic.steps.given import *
from features.arithmetic.steps.when import *
from features.arithmetic.steps.then import *
import time


feature = Feature(
    'Slow Feature',
    Scenario(
        'Slow Scenario',
        given=a_slow_function,
        when=we_call_it_with_the_number_5,
        then=we_will_have_slept
    ),
    Scenario(
        'Slow Scenario',
        given=a_slow_function,
        when=we_call_it_with_the_number_5,
        then=we_will_have_slept
    )
)
feature_two = Feature(
    'Slow Feature',
    Scenario(
        'Slow Scenario',
        given=a_slow_function,
        when=we_call_it_with_the_number_5,
        then=we_will_have_slept
    ),
    Scenario(
        'Slow Scenario',
        given=a_slow_function,
        when=we_call_it_with_the_number_5,
        then=we_will_have_slept
    )
)
# feature = Feature(
#     'Successful Arithmetic',
#     Scenario(
#         'Adding two negative numbers',
#         given=an_adding_function,
#         when=we_call_it_with_two_positive_numbers,
#         then=we_will_get_a_positive_number
#     ),
#     Scenario(
#         'Multiplying two negative numbers',
#         given=a_multiplication_function,
#         when=we_call_it_with_two_negative_numbers,
#         then=we_will_get_a_positive_number
#     )
# )
