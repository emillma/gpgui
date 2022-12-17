from typing import ClassVar, TypeVar
from gpgui.cbtools import CbTypeBase
from dataclasses import dataclass, field
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
class SocketData(CbTypeBase):
    type: str = field(init=False)


@dataclass
class SubscriptionData(SocketData, WithTopiclist):
    type = "subscribe"

    topics: list[str] | str


@dataclass
class UnsubscriptionData(SocketData, WithTopiclist):
    type = "unsubscribe"

    topics: list[str] | str


@dataclass
class PublicationData(SocketData, WithTopiclist):
    type = "publish"

    topics: list[str] | str
    content: str | dict | list
    source: str


@dataclass
class Publication(CbTypeBase):
    data: PublicationData
    origin: str
    isTrusted: bool
    timeStamp: float
