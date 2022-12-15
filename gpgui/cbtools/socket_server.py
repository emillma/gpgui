from quart import Websocket, websocket, abort
from gpgui.cbtools import cbm
import asyncio
import logging


class SocketServer:
    topic_listners: dict[str, set[Websocket]] = {}

    @cbm.websocket("/socketmanager")
    @classmethod
    async def socket_handler(cls):
        headers = websocket.headers
        for topic in headers.getlist("topic"):
            cls.topic_listners.setdefault(topic, []).add(websocket)
        try:
            while True:
                data = await websocket.receive()
                await websocket.send(data)
                await websocket.receive()

        except asyncio.CancelledError as e:
            msg = f"websocket cancelled {str(e)}"
            logging.info(msg)
