from pypattyrn.behavioral.memento import Originator


class Context(Originator):

    def __init__(self, **kwargs):
        self.__dict__['_items'] = dict(**kwargs)

    def __getattr__(self, item):
        try:
            return self._items[item]
        except KeyError:
            raise AttributeError(f'{item} not in Context.')

    def __setattr__(self, key, value):
        self._items[key] = value

    def __str__(self):
        return f"{self.__dict__['_items']}"

    def copy(self):
        return Context(**self.__dict__['_items'])
