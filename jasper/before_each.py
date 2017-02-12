import asyncio
from functools import wraps


class BeforeEach(object):

    def __init__(self, function, **kwargs):
        self.function = function
        self.kwargs = kwargs
        self.ran = False
        self.passed = False

    async def run(self, context):
        context.unlock()
        try:
            if asyncio.iscoroutinefunction(self.function):
                await self.function(context, **self.kwargs)
            else:
                self.function(context, **self.kwargs)
        except Exception as e:
            raise e
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
