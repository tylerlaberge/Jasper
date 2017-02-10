from jasper.exceptions import ThenException
from jasper.utility import cyan, red, grey
from functools import wraps
import asyncio


class Then(object):

    def __init__(self, function, **kwargs):
        self.then_function = function
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

        return color(f'Then: {self.then_function.__name__} {self.kwargs if self.kwargs else ""}')

    async def run(self, context):
        context.lock()
        try:
            if asyncio.iscoroutinefunction(self.then_function):
                await self.then_function(context, **self.kwargs)
            else:
                self.then_function(context, **self.kwargs)
        except Exception as e:
            raise ThenException(e)
        else:
            self.passed = True
        finally:
            self.ran = True


def then(func):
    @wraps(func)
    def wrapper(**kwargs):
        return Then(func, **kwargs)

    return wrapper



