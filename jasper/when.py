from jasper.utility import blue, red, grey
from jasper.exceptions import WhenException
from functools import wraps
from collections import namedtuple
import asyncio


class When(object):

    def __init__(self, function):
        self.when_function = function
        self.ran = False
        self.passed = False

    async def __call__(self, context):
        context.lock()
        try:
            if asyncio.iscoroutinefunction(self.when_function):
                result = await self.when_function(context)
            else:
                result = self.when_function(context)
        except Exception as e:
            raise WhenException(e)
        else:
            context.unlock()
            context.result = result
            self.passed = True
        finally:
            context.lock()
            self.ran = True

    def __str__(self):
        if not self.ran:
            color = grey
        elif self.passed:
            color = blue
        else:
            color = red

        return color(f'When: {self.when_function.__name__}')


def when(func):
    if asyncio.iscoroutinefunction(func):
        @wraps(func)
        async def wrapper(context):
            return_val = await func(context)
            return return_val
    else:
        @wraps(func)
        def wrapper(context):
            return func(context)

    step = namedtuple('Step', ['cls', 'function'])
    return step(cls=When, function=wrapper)

