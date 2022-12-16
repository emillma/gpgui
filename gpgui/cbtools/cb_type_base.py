from dataclasses import dataclass, fields
from typing import Any
import json


@dataclass
class CbTypeBase:
    @classmethod
    def loads(cls, _data: str | dict | None = None, **kwargs):
        obj = object.__new__(cls)

        if isinstance(_data, str):
            data_dict = json.loads(_data)
        elif _data is None:
            data_dict = {}
        else:
            data_dict = _data

        rolled_dict = cls.fix_unrolled_dict(data_dict)
        rolled_dict.update(kwargs)

        fnames = {f.name: f.type for f in fields(obj)}
        for k in rolled_dict.keys() | fnames.keys():
            if k in fnames:
                value = rolled_dict.get(k, None)
                dtype = fnames[k]
                if isinstance(dtype, type) and issubclass(dtype, CbTypeBase):
                    setattr(obj, k, dtype.loads(value))
                elif isinstance(dtype, type) and value:
                    setattr(obj, k, dtype(value))
                else:
                    setattr(obj, k, value)

            else:
                raise TypeError(f"{type(obj).__name__} does not have attribute {k}")
        return obj

    def dumps(self):
        return json.dumps(self.as_dict())

    def as_dict(self):
        output = {}
        for k, v in self.__dict__.items():
            if isinstance(v, CbTypeBase):
                output[k] = v.as_dict()
            else:
                output[k] = v
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

    def toJSON(self):
        return self.dumps()
