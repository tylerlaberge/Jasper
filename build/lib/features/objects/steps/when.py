from jasper import when
from copy import deepcopy


@when
def we_do_nothing(context):
    pass


@when
def we_copy_it(context):
    return deepcopy(context.object)
