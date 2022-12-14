from functools import partial, partialmethod
from typing import Callable, TYPE_CHECKING, Type
from inspect import signature, iscoroutinefunction, _empty
from dataclasses import dataclass

from gpgui.cbtools import Input, Output, State
from gpgui import exceptions
from types import UnionType
from quart import Quart

if TYPE_CHECKING:
    from gpgui import MyDash


@dataclass
class Callback:
    func: Callable
    inputs: dict[str, Input | State]
    outputs: list[Output]
    kwargs: dict


@dataclass
class PyCallback(Callback):
    ...


@dataclass
class JsCallback:
    ...


@dataclass
class Route:
    ...


class CbManager:
    quart: Quart

    pycallbacks: list[PyCallback] = []
    jscallbacks: list[JsCallback] = []

    @classmethod
    def callback(cls, output, **kwargs):
        def decorator(func):
            params = signature(func).parameters
            inputs = {k: v.default for k, v in params.items()}
            assert iscoroutinefunction(func)

            async def inner(**kwargs):
                for k, v in kwargs.items():
                    ann = params[k].annotation
                    if ann is not _empty:
                        if isinstance(ann, UnionType):
                            types = ann.__args__
                            factory = types[0].get_union_factory(types[1:])
                            kwargs[k] = factory(v)
                        else:
                            kwargs[k] = ann(v)
                try:
                    return await func(**kwargs)
                except Exception as e:
                    if isinstance(e, exceptions.PreventUpdate):
                        raise e
                    raise exceptions.CallbackException().with_traceback(e.__traceback__)

            cls.pycallbacks.append(PyCallback(inner, inputs, output, kwargs))
            return func

        return decorator

    @classmethod
    def __getattr__(self, name):
        if name == "quart":
            return None
        return partial(self.callback, name)

    @classmethod
    def register(cls, dash_app: "MyDash"):
        for cb in cls.pycallbacks:
            dash_app.callback(output=cb.outputs, inputs=cb.inputs, **cb.kwargs)(cb.func)
