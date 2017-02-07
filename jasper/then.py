from jasper.exceptions import ThenException
from jasper.utility import blue, red, grey
from functools import wraps
from collections import namedtuple
import asyncio


class Then(object):

    def __init__(self, function):
        self.then_function = function
        self.ran = False
        self.passed = False

    async def __call__(self, context):
        context.lock()
        try:
            if asyncio.iscoroutinefunction(self.then_function):
                await self.then_function(context)
            else:
                self.then_function(context)
        except Exception as e:
            raise ThenException(e)
        else:
            self.passed = True
        finally:
            self.ran = True

    def __str__(self):
        if not self.ran:
            color = grey
        elif self.passed:
            color = blue
        else:
            color = red

        return color(f'Then: {self.then_function.__name__}')


def then(func):
    if asyncio.iscoroutinefunction(func):
        @wraps(func)
        async def wrapper(context):
            await func(context)
    else:
        @wraps(func)
        def wrapper(context):
            func(context)

    step = namedtuple('Step', ['cls', 'function'])
    return step(Then, wrapper)

