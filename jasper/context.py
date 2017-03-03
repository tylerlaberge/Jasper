"""
The context module.
"""

from copy import deepcopy


class Context(object):
    """
    A dictionary-like object where attributes can be accessed using the '.' operator.
    """
    def __init__(self, **kwargs):
        """
        Initialize a new Context object.

        :param kwargs: Keys and values to store into this Context on creation.
        """
        self.__dict__['_items'] = dict(**kwargs)

    def __getattr__(self, item):
        """
        Get an attribute from this Context.

        :param item: The item to get from this Context.
        :return: The item
        :raise: AttributeError: If the item is not in this Context.
        """
        try:
            return self._items[item]
        except KeyError:
            raise AttributeError(f'{item} not in Context.')

    def __setattr__(self, key, value):
        """
        Set an attribute on this Context.

        :param key: The name of the attribute to set.
        :param value: The value of the attribute to set.
        """
        self._items[key] = value

    def __str__(self):
        """
        Get a string representation of this Context.

        :return: A string representation of this Context.
        """
        return f"{self.__dict__['_items']}"

    def copy(self):
        """
        Get a deep copy of this Context.

        :return: A new Context object which is a copy of this Context.
        """
        return Context(**deepcopy(self.__dict__['_items']))
