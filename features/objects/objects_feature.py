from jasper import Feature, Scenario
from features.objects.steps.given import *
from features.objects.steps.when import *
from features.objects.steps.then import *


feature = Feature(
    "Objects",
    Scenario(
        'Dictionary',
        given=a_dictionary_of_data,
        when=we_do_nothing,
        then=this_will_fail_and_we_should_see_the_object
    )
)
