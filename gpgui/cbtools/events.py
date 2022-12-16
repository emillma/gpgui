from dataclasses import dataclass, fields, is_dataclass
from dash_extensions import EventListener  # pylint: disable=unused-import
from .cb_type_base import CbTypeBase


@dataclass
class Target(CbTypeBase):
    """https://developer.mozilla.org/en-US/docs/Web/API/EventTarget"""

    value: str
    children: str
    id: str


@dataclass
class Event(CbTypeBase):
    """https://developer.mozilla.org/en-US/docs/Web/API/Event"""

    target: Target
    timeStamp: float
    type: str

    @classmethod
    def event_dict(cls):
        props = []
        for f in fields(cls):
            if is_dataclass(f.type):
                props.extend(f"{f.name}.{f2.name}" for f2 in fields(f.type))

        return dict(event=cls.__name__, props=props)

    @classmethod
    def get_props(cls):
        return [f.name for f in fields(cls)]

    @classmethod
    def get_union_factory(cls, others: tuple[type]):
        type_dict = {t.__name__: t for t in [cls] + list(others)}

        def factory(value):
            return type_dict[value["type"]](value)

        return factory


@dataclass
class WithModifiers:
    altKey: bool
    shiftKey: bool
    ctrlKey: bool


@dataclass
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


@dataclass
class click(MouseEvent):
    """https://developer.mozilla.org/en-US/docs/Web/API/Element/click_event"""

    ...


@dataclass
class mousedown(MouseEvent):
    """https://developer.mozilla.org/en-US/docs/Web/API/Element/mousedown_event"""

    ...


@dataclass
class mouseup(MouseEvent):
    """https://developer.mozilla.org/en-US/docs/Web/API/Element/mouseup_event"""

    ...


@dataclass
class mousemove(MouseEvent):
    """https://developer.mozilla.org/en-US/docs/Web/API/Element/mousemove_event"""

    ...


@dataclass
class auxclick(MouseEvent):
    """https://developer.mozilla.org/en-US/docs/Web/API/Element/auxclick_event"""

    ...


@dataclass
class dblclick(MouseEvent):
    """https://developer.mozilla.org/en-US/docs/Web/API/Element/dblclick_event"""

    ...


@dataclass
class KeyBoardEvent(Event, WithModifiers):
    """https://developer.mozilla.org/en-US/docs/Web/API/KeyboardEvent"""

    code: str
    key: str
    location: int
    repeat: bool


@dataclass
class keydown(KeyBoardEvent):
    """https://developer.mozilla.org/en-US/docs/Web/API/Element/keydown_event"""

    ...


@dataclass
class keyup(KeyBoardEvent):
    """https://developer.mozilla.org/en-US/docs/Web/API/Element/keyup_event"""

    ...


@dataclass
class keypress(KeyBoardEvent):
    """https://developer.mozilla.org/en-US/docs/Web/API/Element/keypress_event"""

    ...


@dataclass
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
