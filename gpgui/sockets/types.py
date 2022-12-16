from gpgui.cbtools import CbTypeBase
from dataclasses import dataclass

CONNECTING = 0
OPEN = 1
CLOSING = 2
CLOSED = 3


@dataclass
class SocketState(CbTypeBase):
    readyState: int
    isTrusted: bool
    timeStamp: float
    wasClean: bool
    code: int
    reason: str


@dataclass
class Message(CbTypeBase):
    type: str
    data: str | dict


@dataclass
class Publication(CbTypeBase):
    topic: str
    data: str
    # def __init__
