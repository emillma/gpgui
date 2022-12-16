from typing import Type
from quart import Websocket, websocket, abort
from gpgui.cbtools import cbm, CallbackException
from gpgui import idp
import asyncio
import logging
import json

from .annotations import Message


class Webserver:
    topics: dict[str, set[Websocket]] = {}


@cbm.websocket("/<path:topic>")
async def socket_handler(topic):
    assert topic[-2:] == "ws"
    topic_path = topic[:-2]
    headers = websocket.headers

    try:
        while True:
            message = Message(await websocket.receive())

            if message.type == "subscribe":
                for topic in json.loads(message.data):
                    Webserver.topics.setdefault(topic, set()).add(websocket)

            elif message.type == "unsubscribe":
                for topic in json.loads(message.data):
                    Webserver.topics.setdefault(topic, set()).remove(websocket)

            elif message.type == "publish":
                topic = message.data["topic"]
                data = message.data["data"]
                for ws in Webserver.topics[topic]:
                    await ws.send(data)
            else:
                raise CallbackException("unknown message type")

    except asyncio.CancelledError as e:
        msg = f"websocket cancelled {str(e)}"
        for subscribers in Webserver.topics.values():
            subscribers.remove(websocket)
        logging.info(msg)
        return msg

    except Exception as e:
        print(e)
        raise CallbackException(str(e))


@cbm.route("/testroute")
async def testroute():
    return "testroute"
