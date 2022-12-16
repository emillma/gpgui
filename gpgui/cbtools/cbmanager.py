from typing import Callable, TYPE_CHECKING
from types import UnionType
from inspect import signature, iscoroutinefunction, _empty
from dataclasses import dataclass

from dash_extensions.enrich import Input, Output, State

from gpgui import exceptions
from gpgui.cbtools.cb_type_base import CbTypeBase

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
    func: Callable
    rule: str
    defaults: dict | None
    kwargs: dict


@dataclass
class WebSocket:
    func: Callable
    rule: str
    defaults: dict | None
    kwargs: dict


class CbManager:
    registered: bool = False
    pycallbacks: list[PyCallback] = []
    routes: list[Route] = []
    websockets: list[WebSocket] = []
    # jscallbacks: list[JsCallback] = []

    @classmethod
    def callback(cls, output=None, **kwargs):
        assert cls.registered is False

        def decorator(func):
            params = signature(func).parameters
            inputs = {k: v.default for k, v in params.items()}
            assert iscoroutinefunction(func)

            async def wrapped_func(**kwargs):
                # try:
                for k, v in kwargs.items():
                    ann = params[k].annotation
                    if ann is not _empty:
                        if isinstance(ann, UnionType):
                            types = ann.__args__
                            factory = types[0].get_union_factory(types[1:])
                            kwargs[k] = factory(v)
                        else:
                            if issubclass(ann, CbTypeBase):
                                kwargs[k] = ann.loads(v)
                            else:
                                kwargs[k] = ann(v)
                return await func(**kwargs)
                # except Exception as e:
                #     if isinstance(e, exceptions.PreventUpdate):
                #         raise e

                #     raise exceptions.CallbackException(str(e)).with_traceback(
                #         e.__traceback__
                #     ) from e

            cls.pycallbacks.append(PyCallback(wrapped_func, inputs, output, kwargs))
            return func

        return decorator

    @classmethod
    def route(cls, rule: str, defaults: dict | None = None, **kwargs):
        assert cls.registered is False
        if not rule.startswith("/"):
            raise ValueError("urls must start with a leading slash")

        def decorator(func):
            assert iscoroutinefunction(func)
            cls.routes.append(Route(func, rule, defaults, kwargs))
            return func

        return decorator

    @classmethod
    def websocket(cls, rule: str, defaults: dict | None = None, **kwargs):
        assert cls.registered is False

        def decorator(func):
            assert iscoroutinefunction(func)
            cls.websockets.append(WebSocket(func, rule, defaults, kwargs))
            return func

        return decorator

    @classmethod
    def register(cls, dash_app: "MyDash"):
        assert cls.registered is False
        for route in cls.routes:
            dash_app.server.route(
                rule=route.rule, defaults=route.defaults, **route.kwargs
            )(route.func)

        for ws in cls.websockets:
            dash_app.server.websocket(rule=ws.rule, defaults=ws.defaults, **ws.kwargs)(
                ws.func
            )

        for cb in cls.pycallbacks:
            if outputs := cb.outputs:
                dash_app.callback(output=outputs, inputs=cb.inputs, **cb.kwargs)(
                    cb.func
                )
            else:
                dash_app.callback(inputs=cb.inputs, **cb.kwargs)(cb.func)
        cls.registered = True
