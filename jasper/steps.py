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


class Given(Step):
    pass


class When(Step):
    pass


class Then(Step):
    pass


class BeforeEach(Step):
    pass


class AfterEach(Step):
    pass


def given(func):
    @wraps(func)
    def wrapper(**kwargs):
        return Given(func, **kwargs)

    return wrapper


def when(func):
    @wraps(func)
    def wrapper(**kwargs):
        return When(func, **kwargs)

    return wrapper


def then(func):
    @wraps(func)
    def wrapper(**kwargs):
        return Then(func, **kwargs)

    return wrapper


def before_each(func):
    @wraps(func)
    def wrapper(**kwargs):
        return BeforeEach(func, **kwargs)

    return wrapper


def after_each(func):
    @wraps(func)
    def wrapper(**kwargs):
        return AfterEach(func, **kwargs)

    return wrapper




