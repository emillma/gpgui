import aiohttp
import websockets
import asyncio

import websockets.client
from gpgui.sockets.types import Message, Publication


class SocketClient:
    def __init__(
        self,
        name: str,
        url: str,
        listen_to: list[str] | None = None,
        publish_to: list[str] | None = None,
    ):
        self.name = name
        self.url = url
        self.listen_to = listen_to or []
        self.publish_to = publish_to or []
        self.session = aiohttp.ClientSession()
        self.ws: websockets.client.ClientConnection | None = None

    async def __aenter__(self):
        self.ws = await websockets.client.connect(
            self.url, extra_headers={}
        ).__aenter__()

    async def __aexit__(self, exc_type, exc, tb):
        await self.ws.__aexit__(exc_type, exc, tb)

    # async def publish(self,data: dict):
    #     message = Publication(name=self.name, data=data, topic=self.topic)
    #     async with self.session.post(
    #         self.url, json=data, headers={"topic": topic}
    #     ) as resp:
    #         return await resp.json()
