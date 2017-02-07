import time
from jasper import given
import asyncio


@given
def an_exception(context):
    raise Exception


@given
async def a_slow_function(context):
    async def sleep(amount):
        await asyncio.sleep(amount)

    context.sleep = sleep


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
