import re
from typing import TYPE_CHECKING

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
