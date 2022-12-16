from gpgui.cbtools import CbAnnotationBaseClass
import json

CONNECTING = 0
OPEN = 1
CLOSING = 2
CLOSED = 3


class SocketState(CbAnnotationBaseClass):
    readyState: int
    isTrusted: bool
    timeStamp: float
    wasClean: bool
    code: int
    reason: str


class Message(CbAnnotationBaseClass):
    type: str
    data: str
    origin: str
    topic: str


class Publication(CbAnnotationBaseClass):
    topic: str
    data: str
    origin: str

    def __init__(self, _data=None, topic=None, data=None, origin=None):
        super().__init__(_data=_data, topic=topic, data=data, origin=origin)
