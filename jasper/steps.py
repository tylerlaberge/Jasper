from functools import wraps
import asyncio


class Step(object):

    def __init__(self, function, **kwargs):
        self.function = function
        self.kwargs = kwargs
        self.ran = False
        self.passed = False

    async def run(self, context):
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


def step(func):
    @wraps(func)
    def wrapper(**kwargs):
        return Step(func, **kwargs)

    return wrapper
