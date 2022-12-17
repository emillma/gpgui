from typing import Type
from quart import Websocket, websocket, abort
from gpgui.cbtools import cbm
from gpgui import idp
import asyncio
import logging
import json
from .types import SocketData


class Webserver:
    topics: dict[str, set[Websocket]] = {}


@cbm.websocket("/<path:topic>")
async def socket_handler(topic):
    assert topic[-2:] == "ws"
    topic_path = topic[:-2]
    headers = websocket.headers

    try:
        while True:
            message = SocketData.loads(await websocket.receive())

            if message.type == "subsicribe":
                Webserver.topics = json.loads(message.data)
                for topic in Webserver.topics:
                    Webserver.topics.setdefault(topic, set()).add(websocket)

            elif message.type == "unsubscribe":
                Webserver.topics = json.loads(message.data)
                for topic in Webserver.topics:
                    Webserver.topics.setdefault(topic, set()).remove(websocket)

            elif message.type == "publish":
                topic = message.data["topic"]
                data = message.data["data"]
                for ws in Webserver.topics[topic]:
                    await ws.send(data)

    except asyncio.CancelledError as e:
        msg = f"websocket cancelled {str(e)}"
        for subscribers in Webserver.topics.values():
            subscribers.remove(websocket)
        logging.info(msg)
        return msg


@cbm.route("/testroute")
async def testroute():
    return "testroute"
