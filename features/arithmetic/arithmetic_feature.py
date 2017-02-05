from jasper import Feature, Scenario
from features.arithmetic.steps import arithmetic_steps, other_steps


feature = Feature(
    'Arithmetic',
    Scenario(
        'Adding two negative numbers',
        arithmetic_steps.Given('an_adding_function'),
        arithmetic_steps.When('we_call_it_with_two_negative_numbers'),
        arithmetic_steps.Then('we_will_get_a_negative_number')
    ),
    Scenario(
        'Adding two positive numbers',
        arithmetic_steps.Given('an_adding_function'),
        arithmetic_steps.When('we_call_it_with_two_positive_numbers'),
        arithmetic_steps.Then('we_will_get_a_positive_number')
    ),
    Scenario(
        'Multiplying two strings',
        arithmetic_steps.Given('a_multiplication_function'),
        arithmetic_steps.When('we_call_it_with_two_strings'),
        arithmetic_steps.Then('a_typeerror_will_occur')
    ),
    Scenario(
        'Multiplying two positive numbers',
        arithmetic_steps.Given('a_multiplication_function'),
        arithmetic_steps.When('we_call_it_with_two_positive_numbers'),
        arithmetic_steps.Then('we_will_get_a_positive_number')
    ),
    Scenario(
        'Sleeping for a bit',
        arithmetic_steps.Given('a_slow_function'),
        arithmetic_steps.When('we_call_it_with_some_number'),
        arithmetic_steps.Then('we_will_have_slept')
    ),
    Scenario(
        'Multiplying two negative numbers',
        arithmetic_steps.Given('a_multiplication_function'),
        arithmetic_steps.When('we_call_it_with_two_negative_numbers'),
        arithmetic_steps.Then('we_will_get_a_positive_number')
    ),
    Scenario(
        'Using other steps',
        other_steps.Given('some_other_step'),
        other_steps.When('we_call_it'),
        other_steps.Then('we_will_get_foobar')
    )
)
