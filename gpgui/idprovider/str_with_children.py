import re
from typing import TYPE_CHECKING

from dash_extensions.enrich import Input, Output, State

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
        return self._root.register_return(f"{self}-{item}")

    def __call__(self):
        return self

    def as_input(self, prop=None):
        if not prop:
            id_, _, prop = self.rpartition("-")
        else:
            id_ = self

        return Input(id_, prop)

    def as_output(self, prop=None):
        if not prop:
            id_, _, prop = self.rpartition("-")
        else:
            id_ = self
        return Output(id_, prop)

    def as_state(self, prop=None):
        if not prop:
            id_, _, prop = self.rpartition("-")
        else:
            id_ = self

        return State(id_, prop)
