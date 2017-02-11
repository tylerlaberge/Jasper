from pypattyrn.behavioral.memento import Originator
from jasper.exceptions import ContextException


class Context(Originator):

    def __init__(self, **kwargs):
        self.__dict__['_items'] = dict(**kwargs)
        self.__dict__['_locked'] = False

    def __getattr__(self, item):
        try:
            return self._items[item]
        except KeyError:
            raise AttributeError(f'{item} not in Context.')

    def __setattr__(self, key, value):
        if key in self._items:
            raise ContextException("Can't set the same attribute more than once.")
        elif not self.__dict__['_locked']:
            self._items[key] = value
        else:
            raise ContextException("Can't set attributes on a locked Context.")

    def lock(self):
        self.__dict__['_locked'] = True

    def unlock(self):
        self.__dict__['_locked'] = False

