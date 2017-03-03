"""
The steps module.
"""

from functools import wraps
import asyncio


class Step(object):
    """
    The Step class is used as a wrapper around functions for testing behaviours.
    """
    def __init__(self, function, **kwargs):
        """
        Initialize a new Step object.

        :param function: The function this step will call when this step is run.
        :param kwargs: Kwargs to call the given function with.
        """
        self.function = function
        self.kwargs = kwargs
        self.ran = False
        self.passed = False

    async def run(self, context):
        """
        Run this step and record the results.

        :param context: A context object too pass into this steps function.
        """
        try:
            if asyncio.iscoroutinefunction(self.function):
                await self.function(context, **self.kwargs)
            else:
                self.function(context, **self.kwargs)
        except Exception:
            raise
        else:
            self.passed = True
        finally:
            self.ran = True


def step(func):
    """
    A decorator for wrapping a function into a Step object.

    :param func: The function to create a step out of.
    :return: A function which when called will return a new instance of a Step object.
    """
    @wraps(func)
    def wrapper(**kwargs):
        return Step(func, **kwargs)

    return wrapper

