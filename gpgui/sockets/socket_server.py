from dataclasses import dataclass
from typing import Type
from quart import Websocket, websocket, abort
from gpgui.cbtools import cbm, PreventUpdate
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


class SocketServer:
    topics: dict[str, set[Websocket]] = {}


@cbm.websocket("/<path:address>")
async def socket_handler(address):
    headers = websocket.headers
    this_ws = websocket._get_current_object()  # pylint: disable=protected-access
    this_ws: Websocket  # type: ignore

    try:
        while True:
            mdata = await this_ws.receive()

            def hook(thing):
                """make json.loads parse only first layer"""
                return dict(thing)

            message_dict = json.loads(mdata, object_pairs_hook=hook)

            if message := SubscriptionData.loads_if_type(message_dict):
                for topic in message.topics_list():
                    SocketServer.topics.setdefault(topic, set()).add(this_ws)

            elif message := UnsubscriptionData.loads_if_type(message_dict):
                for topic in message.topics_list():
                    SocketServer.topics.setdefault(topic, set()).remove(this_ws)

            elif message := PublicationData.loads_if_type(message_dict):
                for topic in message.topics_list():
                    for ws in SocketServer.topics.get(topic, []):
                        await ws.send(mdata)
            else:
                raise ValueError("Invalid message")

    except asyncio.CancelledError as e:
        msg = f"websocket cancelled {str(e)}"
        logging.info(msg)
        raise e

    except ValueError as value_error:
        await websocket.close(1003, reason=str(value_error))

    finally:
        for subscribers in SocketServer.topics.values():
            subscribers.discard(this_ws)
