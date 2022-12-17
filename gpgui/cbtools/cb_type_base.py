from dataclasses import dataclass, field, fields
from typing import Any, TypeVar
from types import UnionType
import json

T = TypeVar("T", bound="CbTypeBase")


class CbTypeBase:
    _valid: bool = True
    _raw: dict = None

    @classmethod
    def loads(cls: type[T], _data: str, **kwargs) -> T:
        assert isinstance(_data, str)

        obj = cls.load(json.loads(_data), **kwargs)
        obj._raw = _data
        return obj

    @classmethod
    def load(cls: type[T], _data: dict | None, **kwargs) -> T:
        obj = object.__new__(cls)
        obj._raw = obj._raw or _data

        if _data is None:
            obj._valid = False
            return obj

        rolled_dict = cls.fix_unrolled_dict(_data)
        rolled_dict.update(kwargs)

        fields_dict = {f.name: f.type for f in fields(obj)}
        for key in rolled_dict.keys() | fields_dict.keys():
            value = rolled_dict.get(key, None)
            dtype = fields_dict[key]

            if key in fields_dict:
                if key in rolled_dict:
                    if isinstance(dtype, UnionType):
                        setattr(obj, key, value)

                    elif issubclass(dtype, CbTypeBase):
                        if isinstance(value, str):
                            setattr(obj, key, dtype.loads(value))
                        else:
                            setattr(obj, key, dtype.load(value))

                    else:
                        setattr(obj, key, dtype(value))

                else:
                    setattr(obj, key, None)

            else:
                raise TypeError(f"{type(obj).__name__} does not have attribute {key}")
        return obj

    def dumps(self):
        return json.dumps(self.dump())

    def dump(self):
        output = {}
        for field in fields(self):
            value = getattr(self, field.name)
            if isinstance(value, CbTypeBase):
                output[field.name] = value.dump()
            else:
                output[field.name] = value
        return output

    @classmethod
    def fix_unrolled_dict(cls, unrolled_dict: dict):
        rolled_dict: dict[str, dict | Any] = {}
        for key, value in unrolled_dict.items():
            pre, _, post = key.partition(".")
            if post:
                rolled_dict.setdefault(pre, {})[post] = value
            else:
                rolled_dict[key] = value
        return rolled_dict

    def __repr__(self):
        fields = ", ".join(f"{k}={v}" for k, v in self.__dict__.items())
        return f"{self.__class__.__name__}({fields})"

    def __bool__(self):
        return bool(self._valid)

    def toJSON(self):
        return self.dumps()
