import time
from jasper import given


@given
def an_exception(context):
    raise Exception


@given
def a_slow_function(context):
    def sleep(amount):
        time.sleep(amount)

    context['sleep'] = sleep


@given
def an_adding_function(context):
    def add(a, b):
        return a + b

    context.function = add


@given
def a_multiplication_function(context):
    def multiply(a, b):
        return a * b

    context.function = multiply
