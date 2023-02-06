import aiohttp
import asyncio

import websockets.client
from gpgui.config import PORT, HOST
import json
import types


class SocketClientPubSub:
    def __init__(
        self,
        pub: str | list[str] | None = None,
        sub: str | list[str] | None = None,
    ):
        self.pub = [pub] if isinstance(pub, str) else pub or []
        self.sub = [sub] if isinstance(sub, str) else sub or []
        pub_str = "&".join(f"pub={p}" for p in self.pub)
        sub_str = "&".join(f"sub={s}" for s in self.sub)

        url = f"ws://{HOST}:{PORT}/testsocket?{pub_str}&{sub_str}"

        self.connection = websockets.client.connect(url, extra_headers={})
        self.ws: websockets.client.WebSocketClientProtocol | None = None

    async def __aenter__(self):
        self.ws = await self.connection.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.connection.__aexit__(exc_type, exc, tb)
        self.ws = None

    async def send(self, data: dict | str | list):
        assert self.ws is not None
        if not isinstance(data, str):
            data = json.dumps(data)
        await self.ws.send(data)

    async def recv(self):
        assert self.ws is not None
        data = await self.ws.recv()
        try:
            return json.loads(data)
        except json.JSONDecodeError:
            return data

    def send_sync(self, data: dict | str | list):
        async def inner():
            async with self:
                await self.send(data)

        asyncio.run(inner())

    async def recv_sync(self, timeout=1):
        async def inner():
            async with self:
                return await self.recv()

        return asyncio.run(asyncio.wait_for(inner(), timeout=timeout))
