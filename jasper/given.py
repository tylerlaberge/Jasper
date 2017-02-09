from jasper.utility import blue, red
from jasper.exceptions import GivenException
from functools import wraps
import asyncio


class Given(object):

    def __init__(self, function):
        self.given_function = function
        self.passed = False

    async def __call__(self, context):
        context.unlock()
        try:
            if asyncio.iscoroutinefunction(self.given_function):
                await self.given_function(context)
            else:
                self.given_function(context)
        except Exception as e:
            raise GivenException(e)
        else:
            self.passed = True
        finally:
            context.lock()

    def __str__(self):
        color = blue if self.passed else red

        return color(f"Given: {self.given_function.__name__}")


def given(func):
    if asyncio.iscoroutinefunction(func):
        @wraps(func)
        async def wrapper(context):
            await func(context)
    else:
        @wraps(func)
        def wrapper(context):
            func(context)

    return Given(wrapper)



