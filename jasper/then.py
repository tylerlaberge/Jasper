from functools import wraps
import asyncio


class Then(object):

    def __init__(self, function, **kwargs):
        self.function = function
        self.kwargs = kwargs
        self.ran = False
        self.passed = False

    async def run(self, context):
        context.lock()
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


def then(func):
    @wraps(func)
    def wrapper(**kwargs):
        return Then(func, **kwargs)

    return wrapper



