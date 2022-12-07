import re


class StrWithChildren(str):
    _register_func: callable
    _pos_func: callable

    def __new__(self, value, register_func, pos_func):
        obj = str.__new__(self, value)
        obj._register_func = register_func
        obj._pos_func = pos_func
        return obj

    def __getattr__(self, item):
        if re.match("__.*__", item):
            raise AttributeError(item)
        return self._register_func(f"{self}.{item}")

    def pos(self):
        return self._pos_func(self)

    def posprint(self):
        """Print the positions of the known IDs."""
        for pos in self.pos():
            print(pos)
