from functools import wraps
import asyncio


class Then(object):

    def __init__(self, function, **kwargs):
        self.then_function = function
        self.kwargs = kwargs
        self.ran = False
        self.passed = False

    async def run(self, context):
        context.lock()
        try:
            if asyncio.iscoroutinefunction(self.then_function):
                await self.then_function(context, **self.kwargs)
            else:
                self.then_function(context, **self.kwargs)
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



