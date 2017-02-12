from jasper import Feature, Scenario
from features.given.steps.given import *
from features.given.steps.when import *
from features.given.steps.then import *
from features.given.steps.before_each import *


feature = Feature(
    'Given Class Feature',
    Scenario(
        'Initialization',
        given=[
            some_function(),
            some_kwargs(kwargs={'foo': 'bar'})
        ],
        when=we_initialize_a_given_object_with_it(),
        then=[
            the_given_object_should_use_the_given_function(),
            the_given_object_should_use_the_given_kwargs()
        ]
    ),
    Scenario(
        'Successful Run',
        given=an_initialized_given_object(given_function_kwargs={'foo': 'bar'}),
        when=we_run_it_with_some_context(),
        then=[
            the_given_step_should_have_passed(),
            the_given_function_should_have_been_called_with(given_function_kwargs={'foo': 'bar'})
        ]
    ),
    Scenario(
        'Failing Run',
        given=an_initialized_given_object_with_a_function_that_will_fail(),
        when=we_run_it_and_are_prepared_for_an_exception(),
        then=[
            an_exception_should_have_been_raised(),
            the_given_step_should_have_failed()
        ]
    ),
    Scenario(
        'Successful Async Run',
        given=an_initialized_given_object_with_an_async_function(given_function_kwargs={'bar': 'foo'}),
        when=we_run_it_with_some_context(),
        then=[
            the_given_function_should_have_been_called_with(given_function_kwargs={'bar': 'foo'}),
            the_given_step_should_have_passed()
        ]
    ),
    Scenario(
        'Passing String Representation',
        given=an_initialized_given_object(ran=True, passed=True, given_function_kwargs={'foo': 'bar'}),
        when=we_get_a_string_representation_of_the_given_object(),
        then=it_should_be_colored_cyan_and_display_its_attributes(given_function_kwargs={'foo': 'bar'})
    ),
    Scenario(
        'Failing String Representation',
        given=an_initialized_given_object(ran=True, passed=False, given_function_kwargs={'bar': 'foo'}),
        when=we_get_a_string_representation_of_the_given_object(),
        then=it_should_be_colored_red_and_display_its_attributes(given_function_kwargs={'bar': 'foo'})
    ),
    Scenario(
        'Before Each',
        given=nothing(),
        when=we_do_nothing(),
        then=there_should_be_foo_data()
    ),
    before_each=prepare_some_foo_data()
)
