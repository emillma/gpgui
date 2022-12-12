from typing import Callable, TYPE_CHECKING
from inspect import signature, iscoroutinefunction
from dataclasses import dataclass

from gpgui.cbtools import Input, Output, State

if TYPE_CHECKING:
    from gpgui import MyDash


@dataclass
class PyCallback:
    func: Callable
    inputs: dict[str, Input | State]
    outputs: list[Output]


class JsCallback:
    ...


class Route:
    ...


class CbManager:
    pycallbacks: list[PyCallback] = []
    jscallbacks: list[JsCallback] = []
    routes: list[Route] = []

    @classmethod
    def callback(cls, output):
        def decorator(func):
            params = signature(func).parameters
            inputs = {k: v.default for k, v in params.items()}
            assert iscoroutinefunction(func)

            async def inner(**kwargs):
                return func(**kwargs)

            cls.pycallbacks.append(PyCallback(func, inputs, output))
            return inner

        return decorator

    @classmethod
    def register(cls, dash_app: "MyDash"):
        for pycb in cls.pycallbacks:
            dash_app.callback(output=pycb.outputs, inputs=pycb.inputs)(pycb.func)
            # if len(args) == 1:
            #     dash_app.callback(func)
            # else:
            #     dash_app.callback(*args[1:])(func)
