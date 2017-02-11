from jasper.utility import cyan, red, grey
from jasper.exceptions import WhenException
from functools import wraps
import asyncio


class When(object):

    def __init__(self, function, **kwargs):
        self.when_function = function
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

        return color(f'When: {self.when_function.__name__} {self.kwargs if self.kwargs else ""}')

    async def run(self, context):
        context.unlock()
        try:
            if asyncio.iscoroutinefunction(self.when_function):
                await self.when_function(context, **self.kwargs)
            else:
                self.when_function(context, **self.kwargs)
        except Exception as e:
            raise WhenException(e)
        else:
            self.passed = True
        finally:
            context.lock()
            self.ran = True


def when(func):
    @wraps(func)
    def wrapper(**kwargs):
        return When(func, **kwargs)

    return wrapper


