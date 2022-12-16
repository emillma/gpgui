from dataclasses import dataclass
from typing import Type
from quart import Websocket, websocket, abort
from gpgui.cbtools import cbm, CallbackException
from gpgui import idp
from gpgui.sockets.types import (
    Message,
    PublicationMessage,
    SubscriptionMessage,
    UnsubscriptionMessage,
)
import asyncio
import logging
import json

from gpgui.sockets.types import Message


class SocketServer:
    topics: dict[str, set[Websocket]] = {}


@cbm.websocket("/<path:topic>")
async def socket_handler(topic):
    assert topic[-2:] == "ws"
    topic_path = topic[:-2]
    headers = websocket.headers
    event = asyncio.Event()
    this_socket: Websocket = websocket._get_current_object()
    try:
        while True:
            mdata = await this_socket.receive()
            mtype = mdata[: Message.TYPEIDLEN]

            if mtype == SubscriptionMessage.TYPEID:
                message = SubscriptionMessage.loads(mdata)
                for topic in message.topics_list():  # pylint: disable=no-member
                    SocketServer.topics.setdefault(topic, set()).add(this_socket)

            elif mtype == UnsubscriptionMessage.TYPEID:
                message = UnsubscriptionMessage.loads(mdata)
                for topic in message.topics_list():  # pylint: disable=no-member
                    SocketServer.topics.setdefault(topic, set()).remove(this_socket)

            elif mtype == PublicationMessage.TYPEID:
                message = PublicationMessage.loads(mdata)
                for topic in message.topics_list():  # pylint: disable=no-member
                    for ws in SocketServer.topics[topic]:
                        await ws.send(mdata)
            else:
                raise CallbackException("unknown message type")

    except (asyncio.CancelledError, KeyError) as e:
        msg = f"websocket cancelled {str(e)}"
        for subscribers in SocketServer.topics.values():
            subscribers.remove(this_socket)
        logging.info(msg)
        return msg

    except BaseException as e:
        raise CallbackException(str(e)) from e


@cbm.route("/testroute")
async def testroute():
    return "testroute"
