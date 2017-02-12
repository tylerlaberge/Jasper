from functools import wraps
import asyncio


class When(object):

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
            context.lock()
            self.ran = True


def when(func):
    @wraps(func)
    def wrapper(**kwargs):
        return When(func, **kwargs)

    return wrapper


