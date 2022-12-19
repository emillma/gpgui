import aiohttp
import asyncio

import websockets.client
from gpgui.sockets.types import SocketData, PublicationData


class SocketClient:
    def __init__(
        self,
        name: str,
        url: str,
        listen_to: list[str] | None = None,
        publish_to: list[str] | None = None,
    ):
        self.name = name
        print(url)
        self.url = url
        self.listen_topics = listen_to or []
        self.publish_topics = publish_to or []

        self.connection = websockets.client.connect(self.url, extra_headers={})
        self.ws: websockets.client.WebSocketClientProtocol | None = None

    async def __aenter__(self):
        self.ws = await self.connection.__aenter__()

    async def __aexit__(self, exc_type, exc, tb):
        await self.connection.__aexit__(exc_type, exc, tb)
        self.ws = None

    async def publish(self, data: dict | str | list):
        assert isinstance(self.ws, websockets.client.WebSocketClientProtocol)
        message = PublicationData(
            topics=self.publish_topics, data=data, source=self.name
        )
        print(message.dumps())
        await self.ws.send(message.dumps())

    # def publish_synchronous(self, data: dict | str | list):
    #     return unsync(self.publish)(data)
