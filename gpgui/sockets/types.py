from typing import ClassVar, TypeVar
from gpgui.cbtools import CbTypeBase
from dataclasses import dataclass
import json

CONNECTING = 0
OPEN = 1
CLOSING = 2
CLOSED = 3

T = TypeVar("T", bound="Message")


class WithTopiclist:
    topics: str | list[str]

    def topics_list(self):
        return self.topics if isinstance(self.topics, list) else [self.topics]


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
    TYPEID: ClassVar[str]
    TYPEIDLEN = 4

    def dumps(self):
        assert len(self.TYPEID) == 4
        return self.TYPEID + json.dumps(self.__dict__)

    @classmethod
    def loads(cls: type[T], _data: str, **kwargs) -> T:
        if _data is None:
            return super().loads(None, **kwargs)
        assert _data[:4] == cls.TYPEID
        return super().loads(_data[4:], **kwargs)


@dataclass
class SubscriptionMessage(Message, WithTopiclist):
    TYPEID = "sub+"

    topics: list[str] | str
    type: str = "subscribe"


@dataclass
class UnsubscriptionMessage(Message, WithTopiclist):
    TYPEID = "sub-"

    topics: list[str] | str
    type: str = "unsubscribe"


@dataclass
class PublicationMessage(Message, WithTopiclist):
    TYPEID = "pub_"
    topics: list[str] | str
    data: str | dict | list
    source: str
    type: str = "publish"


@dataclass
class Publication(CbTypeBase):
    data: PublicationMessage
    origin: str
    isTrusted: bool
    timeStamp: float
