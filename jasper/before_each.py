import asyncio
from functools import wraps
from jasper.exceptions import BeforeException
from jasper.utility import grey, cyan, red


class BeforeEach(object):

    def __init__(self, function, **kwargs):
        self.function = function
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

        return color(f'BeforeEach: {self.function.__name__} {self.kwargs if self.kwargs else ""}')

    async def run(self, context):
        context.unlock()
        try:
            if asyncio.iscoroutinefunction(self.function):
                await self.function(context, **self.kwargs)
            else:
                self.function(context, **self.kwargs)
        except Exception as e:
            raise BeforeException(e)
        else:
            self.passed = True
        finally:
            self.ran = True
            context.lock()


def before_each(func):
    @wraps(func)
    def wrapper(**kwargs):
        return BeforeEach(func, **kwargs)

    return wrapper
