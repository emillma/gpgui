from typing import ClassVar, Type, TypeVar
from gpgui.cbtools import CbTypeBase
from dataclasses import dataclass, field
import json

CONNECTING = 0
OPEN = 1
CLOSING = 2
CLOSED = 3

# T = TypeVar("T", bound="SocketData")

@dataclass
class Message(CbTypeBase):
    data: str = field(default=None)
    origin: str = field(default=None)
    isTrusted: bool = field(default=None)
    timeStamp: float = field(default=None)

# @dataclass
# class SocketData(CbTypeBase):
#     type: str = field(init=False)

#     @classmethod
#     def loads_if_type(cls: Type[T], _data: dict) -> T | None:
#         if _data.get("type") == cls.type:
#             return cls.load(_data)
#         return None


# @dataclass
# class WithTopiclist:
#     topics: list[str] = field(kw_only=True, default_factory=list)

#     def topics_list(self):
#         return self.topics


# @dataclass
# class SocketState(CbTypeBase):
#     readyState: int
#     isTrusted: bool
#     timeStamp: float
#     wasClean: bool
#     code: int
#     reason: str


# @dataclass
# class SubscriptionData(SocketData, WithTopiclist):
#     type = "subscribe"


# @dataclass
# class UnsubscriptionData(SocketData, WithTopiclist):
#     type = "unsubscribe"


# @dataclass
# class PublicationData(SocketData, WithTopiclist):
#     type = "publish"
#     data: str | dict | list
#     source: str | None


