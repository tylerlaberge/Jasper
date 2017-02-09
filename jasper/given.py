from jasper.utility import blue, red
from jasper.exceptions import GivenException
from functools import wraps
import asyncio


class Given(object):

    def __init__(self, function, **kwargs):
        self.given_function = function
        self.kwargs = kwargs
        self.passed = False

    def __str__(self):
        color = blue if self.passed else red

        return color(f"Given: {self.given_function.__name__} {self.kwargs if self.kwargs else ''}")

    async def run(self, context):
        context.unlock()
        try:
            if asyncio.iscoroutinefunction(self.given_function):
                await self.given_function(context, **self.kwargs)
            else:
                self.given_function(context, **self.kwargs)
        except Exception as e:
            raise GivenException(e)
        else:
            self.passed = True
        finally:
            context.lock()


def given(func):
    @wraps(func)
    def wrapper(**kwargs):
        return Given(func, **kwargs)

    return wrapper




