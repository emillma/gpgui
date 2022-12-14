from functools import partial, partialmethod
from typing import Callable, TYPE_CHECKING
from inspect import signature, iscoroutinefunction, _empty
from dataclasses import dataclass

from gpgui.cbtools import Input, Output, State
from gpgui import exceptions
from types import UnionType

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


class JsCallback:
    ...


class Route:
    ...


class CbManager:
    pycallbacks: list[PyCallback] = []
    jscallbacks: list[JsCallback] = []
    routes: list[Route] = []

    @classmethod
    def callback(cls, output, **kwargs):
        def decorator(func):
            params = signature(func).parameters
            inputs = {k: v.default for k, v in params.items()}
            assert iscoroutinefunction(func)

            async def inner(**kwargs):
                for k, v in kwargs.items():
                    ann = params[k].annotation
                    assert ann is not _empty, f"Missing type annotation for {k}"
                    if isinstance(ann, UnionType):
                        types = ann.__args__
                        factory = types[0].get_union_factory(types[1:])
                        kwargs[k] = factory(v)
                    else:
                        kwargs[k] = ann(v)
                return await func(**kwargs)
                # try:
                #     output = await func(**kwargs)
                #     return output
                # except Exception as e:
                #     raise exceptions.CallbackException(str(e))

            cls.pycallbacks.append(PyCallback(inner, inputs, output, kwargs))
            return func

        return decorator

    # def

    @classmethod
    def register(cls, dash_app: "MyDash"):
        for cb in cls.pycallbacks:
            dash_app.callback(output=cb.outputs, inputs=cb.inputs, **cb.kwargs)(cb.func)
