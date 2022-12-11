import re
from typing import TYPE_CHECKING

from gpgui.cbtools import Input, Output, State

if TYPE_CHECKING:
    from .idprovider import IdProvider


class StrWithChildren(str):
    _root: "IdProvider"

    def __new__(cls, value, root: "IdProvider"):
        obj = str.__new__(cls, value)
        obj._root = root
        return obj

    def __getattr__(self, item):
        if re.match("__.*__", item):
            raise AttributeError(item)
        return self._root.register_return(f"{self}.{item}")

    def __call__(self):
        return self

    def input(self, prop):
        return Input(self, prop)

    def output(self, prop):
        return Output(self, prop)

    def state(self, prop):
        return State(self, prop)
