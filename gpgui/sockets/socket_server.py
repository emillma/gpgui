from dataclasses import dataclass
from typing import Type
from quart import Websocket, websocket, abort
from gpgui.cbtools import cbm, CallbackException
from gpgui import idp
from gpgui.sockets.types import (
    SocketData,
    PublicationData,
    SubscriptionData,
    UnsubscriptionData,
)
import asyncio
import logging
import json
from json.decoder import JSONDecoder

from gpgui.sockets.types import SocketData


class SocketServer:
    topics: dict[str, set[Websocket]] = {}


@cbm.websocket("/<path:address>")
async def socket_handler(address):
    headers = websocket.headers
    this_socket: Websocket = websocket._get_current_object()
    try:
        while True:
            mdata = await this_socket.receive()

            def hook(thing):
                return dict(thing)

            message = json.loads(mdata, object_pairs_hook=hook)

            mtype = message["type"]
            if mtype == SubscriptionData.type:
                message = SubscriptionData.loads(mdata)
                for topic in message.topics_list():
                    SocketServer.topics.setdefault(topic, set()).add(this_socket)

            elif mtype == UnsubscriptionData.type:
                message = UnsubscriptionData.loads(mdata)
                for topic in message.topics_list():
                    SocketServer.topics.setdefault(topic, set()).remove(this_socket)

            elif mtype == PublicationData.type:
                message = PublicationData.loads(mdata)
                for topic in message.topics_list():
                    for ws in SocketServer.topics.get(topic, []):
                        await ws.send(mdata)
            else:
                raise CallbackException("unknown message type")

    except asyncio.CancelledError as e:
        msg = f"websocket cancelled {str(e)}"
        for subscribers in SocketServer.topics.values():
            subscribers.discard(this_socket)
        logging.info(msg)
        raise


@cbm.route("/testroute")
async def testroute():
    return "testroute"
