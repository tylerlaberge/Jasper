from functools import wraps
import asyncio


class Step(object):

    def __init__(self, step_type, function, **kwargs):
        self.step_type = step_type
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


def given(func):
    @wraps(func)
    def wrapper(**kwargs):
        return Step('Given', func, **kwargs)

    return wrapper


def when(func):
    @wraps(func)
    def wrapper(**kwargs):
        return Step('When', func, **kwargs)

    return wrapper


def then(func):
    @wraps(func)
    def wrapper(**kwargs):
        return Step('Then', func, **kwargs)

    return wrapper


def before_each(func):
    @wraps(func)
    def wrapper(**kwargs):
        return Step('BeforeEach', func, **kwargs)

    return wrapper


def after_each(func):
    @wraps(func)
    def wrapper(**kwargs):
        return Step('AfterEach', func, **kwargs)

    return wrapper




