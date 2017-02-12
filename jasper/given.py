from jasper.utility import cyan, red, grey
from functools import wraps
import asyncio


class Given(object):

    def __init__(self, function, **kwargs):
        self.given_function = function
        self.kwargs = kwargs
        self.ran = False
        self.passed = False

    def __str__(self):
        if not self.ran:
            color = grey
        elif self.passed:
            color = cyan
        else:
            color = red

        return color(f"Given: {self.given_function.__name__} {self.kwargs if self.kwargs else ''}")

    async def run(self, context):
        context.unlock()
        try:
            if asyncio.iscoroutinefunction(self.given_function):
                await self.given_function(context, **self.kwargs)
            else:
                self.given_function(context, **self.kwargs)
        except Exception as e:
            raise e
        else:
            self.passed = True
        finally:
            self.ran = True
            context.lock()


def given(func):
    @wraps(func)
    def wrapper(**kwargs):
        return Given(func, **kwargs)

    return wrapper




