import json
from typing import Any
import inspect


class CbAnnotationBaseClass:
    def __init__(self, _data: str | dict | None = None, **kwargs):
        if isinstance(_data, str):
            data_dict = json.loads(_data)
        elif _data is None:
            data_dict = {}
        else:
            data_dict = _data

        rolled_dict = self.fix_unrolled_dict(data_dict)
        rolled_dict.update(kwargs)

        ann = self.annotations()
        for k in rolled_dict.keys() | ann.keys():
            if k in ann:
                value = rolled_dict.get(k, None)
                dtype = ann[k]
                if value or issubclass(dtype, CbAnnotationBaseClass):
                    setattr(self, k, dtype(value))
                else:
                    setattr(self, k, value)

            else:
                raise TypeError(f"{type(self).__name__} does not have attribute {k}")

    def dumps(self):
        return json.dumps(self.as_dict())

    def as_dict(self):
        output = {}
        for k, v in self.__dict__.items():
            if isinstance(v, CbAnnotationBaseClass):
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

    @classmethod
    def annotations(cls):
        return dict(j for i in cls.__mro__[:-1] for j in i.__annotations__.items())

    def __repr__(self):
        fields = ", ".join(f"{k}={v}" for k, v in self.__dict__.items())
        return f"{self.__class__.__name__}({fields})"

    def toJSON(self):
        return self.dumps()
