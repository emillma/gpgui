from typing import Any, Union
from dataclasses import dataclass


class InitFromDict:
    def __init__(self, event_dict: dict | None):
        event_dict = event_dict or {}
        fixed_dict: dict[str, dict | Any] = {}
        for key, value in event_dict.items():
            pre, _, post = key.partition(".")
            if post:
                fixed_dict.setdefault(pre, {})[post] = value
            else:
                fixed_dict[key] = value

        ann = self.annotations()
        for k in fixed_dict.keys() | ann.keys():
            if k in ann:
                value = fixed_dict.get(k, None)
                dtype = ann[k]
                if value or issubclass(dtype, InitFromDict):
                    setattr(self, k, dtype(value))
                else:
                    setattr(self, k, value)

            else:
                raise TypeError(f"Unexpected key {k} in event_dict")

    @classmethod
    def annotations(cls):
        return dict(j for i in cls.__mro__[:-1] for j in i.__annotations__.items())

    def __repr__(self):
        fields = ", ".join(f"{k}={v}" for k, v in self.__dict__.items())
        return f"{self.__class__.__name__}({fields})"


class Target(InitFromDict):
    """https://developer.mozilla.org/en-US/docs/Web/API/EventTarget"""

    value: str
    children: str
    id: str


class Event(InitFromDict):
    """https://developer.mozilla.org/en-US/docs/Web/API/Event"""

    target: Target
    timeStamp: float
    type: str

    @classmethod
    def event_dict(cls):
        props = []
        todo = list(cls.annotations().items())
        while todo:
            k, v = todo.pop()
            if annotations := getattr(v, "__annotations__", None):
                props.extend(f"{k}.{ann}" for ann in annotations)
            else:
                props.append(k)

        return dict(event=cls.__name__, props=props)

    @classmethod
    def get_union_factory(cls, others: tuple[type]):
        type_dict = {t.__name__: t for t in [cls] + list(others)}

        def factory(value):
            return type_dict[value["type"]](value)

        return factory


class WithModifiers:
    altKey: bool
    shiftKey: bool
    ctrlKey: bool


class MouseEvent(Event, WithModifiers):
    """https://developer.mozilla.org/en-US/docs/Web/API/MouseEvent"""

    button: str
    buttons: str
    clientX: int
    clientY: int
    movementX: int
    movementY: int
    offsetX: int
    offsetY: int
    pageX: int
    pageY: int
    screenX: int
    screenY: int
    x: int
    y: int


class click(MouseEvent):
    """https://developer.mozilla.org/en-US/docs/Web/API/Element/click_event"""

    ...


class mousedown(MouseEvent):
    """https://developer.mozilla.org/en-US/docs/Web/API/Element/mousedown_event"""

    ...


class mouseup(MouseEvent):
    """https://developer.mozilla.org/en-US/docs/Web/API/Element/mouseup_event"""

    ...


class mousemove(MouseEvent):
    """https://developer.mozilla.org/en-US/docs/Web/API/Element/mousemove_event"""

    ...


class auxclick(MouseEvent):
    """https://developer.mozilla.org/en-US/docs/Web/API/Element/auxclick_event"""

    ...


class dblclick(MouseEvent):
    """https://developer.mozilla.org/en-US/docs/Web/API/Element/dblclick_event"""

    ...


class KeyBoardEvent(Event, WithModifiers):
    """https://developer.mozilla.org/en-US/docs/Web/API/KeyboardEvent"""

    code: str
    key: str
    location: int
    repeat: bool


class keydown(KeyBoardEvent):
    """https://developer.mozilla.org/en-US/docs/Web/API/Element/keydown_event"""

    ...


class keyup(KeyBoardEvent):
    """https://developer.mozilla.org/en-US/docs/Web/API/Element/keyup_event"""

    ...


class keypress(KeyBoardEvent):
    """https://developer.mozilla.org/en-US/docs/Web/API/Element/keypress_event"""

    ...


class change(Event):
    """https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/change_event"""

    ...


EventType = (
    mousemove
    | click
    | mousedown
    | mouseup
    | auxclick
    | dblclick
    | keydown
    | keyup
    | keypress
)
