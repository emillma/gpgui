from typing import Callable
from inspect import signature
from dataclasses import dataclass

from gpgui import MyDash
from gpgui.cbtools import Input, Output, State
from typing import Union


@dataclass
class PyCallback:
    func: Callable
    inputs: dict[str, Input, State]
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
            inputs = {k: v.default for k, v in signature(func).parameters.items()}
            cls.pycallbacks.append(PyCallback(func, inputs, output))
            return func

        return decorator

    @classmethod
    def register(cls, dash_app: MyDash):
        for pycb in cls.pycallbacks:
            dash_app.callback(output=pycb.outputs, inputs=pycb.inputs)(pycb.func)
            # if len(args) == 1:
            #     dash_app.callback(func)
            # else:
            #     dash_app.callback(*args[1:])(func)
